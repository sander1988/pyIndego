""" API for Bosch API server for Indego lawn mower """
import asyncio
import json
import logging
import typing

import aiohttp

# from aiohttp import hdrs
import requests

# from aiofile import AIOFile
from aiohttp import ClientResponseError
from aiohttp import ServerTimeoutError
from aiohttp import TooManyRedirects
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPGatewayTimeout
from aiohttp.helpers import BasicAuth

from . import __version__
from .const import Methods
from .const import COMMANDS
from .const import CONTENT_TYPE_JSON
from .const import DEFAULT_BODY
from .const import DEFAULT_CALENDAR
from .const import DEFAULT_HEADER
from .const import DEFAULT_URL
from .indego_base_client import IndegoBaseClient

_LOGGER = logging.getLogger(__name__)


class IndegoAsyncClient(IndegoBaseClient):
    """Class for Indego Async Client."""

    def __init__(
        self,
        username: str,
        password: str,
        serial: str,
        map_filename: str = None,
        api_url: str = DEFAULT_URL,
    ):
        """Initialize the Async Client

        Args:
            username (str): username for Indego Account
            password (str): password for Indego Account
            serial (str): serial number of the mower
            map_filename (str, optional): Filename to store maps in. Defaults to None.
            api_url (str, optional): url for the api, defaults to DEFAULT_URL.
            
        """
        super().__init__(username, password, serial, map_filename, api_url)
        self._session = aiohttp.ClientSession(raise_for_status=False)

    async def __aenter__(self):
        """Enter for async with."""
        await self.start()
        return self

    async def __aexit__(self, type, value, traceback):
        """Exit for async with."""
        await self.close()

    async def start(self):
        """Login if not done."""
        if not self._logged_in:
            await self.login()

    async def close(self):
        """Close the aiohttp session."""
        await self._session.close()

    async def update_all(self, force=False):
        """Update all states."""
        results = await asyncio.gather(
            *[
                self.update_generic_data(),
                self.update_alerts(),
                self.update_last_completed_mow(),
                self.update_location(),
                self.update_next_mow(),
                self.update_operating_data(),
                self.update_state(force),
                self.update_updates_available(),
                self.update_users(),
                self.update_network(),
            ],
            return_exceptions=True,
        )
        for res in results:
            if res:
                _LOGGER.warning(res)

    async def update_generic_data(self):
        """Update generic data."""
        self._update_generic_data(await self.get(f"alms/{self._serial}"))

    async def update_alerts(self):
        """Update alerts."""
        self._update_alerts(await self.get("alerts"))

    async def update_last_completed_mow(self):
        """Update last completed mow."""
        self._update_last_completed_mow(
            await self.get(f"alms/{self._serial}/predictive/lastcutting")
        )

    async def update_location(self):
        """Update location."""
        self._update_location(
            await self.get(f"alms/{self._serial}/predictive/location")
        )

    async def update_next_mow(self):
        """Update next mow datetime."""
        self._update_next_mow(
            await self.get(f"alms/{self._serial}/predictive/nextcutting")
        )

    async def update_operating_data(self):
        """Update operating data."""
        self._update_operating_data(
            await self.get(f"alms/{self._serial}/operatingData")
        )

    async def update_state(self, force=False, longpoll=False, longpoll_timeout=120):
        """Update state. Can be both forced and with longpoll.

        Args:
            force (bool, optional): Force the state refresh, wakes up the mower. Defaults to False.
            longpoll (bool, optional): Do a longpoll. Defaults to False.
            longpoll_timeout (int, optional): Timeout of the longpoll. Defaults to 120.

        """
        path = f"alms/{self._serial}/state"
        if longpoll:
            last_state = 0
            if self.state.state:
                last_state = self.state.state
            path = f"{path}?longpoll=true&timeout={longpoll_timeout}&last={last_state}"
        if force:
            if longpoll:
                path = f"{path}&forceRefresh=true"
            else:
                path = f"{path}?forceRefresh=true"

        self._update_state(await self.get(path, timeout=longpoll_timeout + 30))

    async def update_updates_available(self):
        """Update updates available."""
        if self._online:
            self._update_updates_available(
                await self.get(f"alms/{self._serial}/updates")
            )

    async def update_users(self):
        """Update users."""
        self._update_users(await self.get(f"users/{self._userid}"))

    async def update_network(self):
        """Update network."""
        self._update_network(await self.get(f"alms/{self._serial}/network"))

    async def update_config(self):
        """Update config."""
        self._update_config(await self.get(f"alms/{self._serial}/config"))

    async def update_setup(self):
        """Update setup."""
        self._update_setup(await self.get(f"alms/{self._serial}/setup"))

    async def update_security(self):
        """Update security."""
        self._update_security(await self.get(f"alms/{self._serial}/security"))

    async def download_map(self, filename: str = None):
        """Download the map.

        Args:
            filename (str, optional): Filename for the map. Defaults to None, can also be filled by the filename set in init.

        """
        if filename:
            self.map_filename = filename
        if not self.map_filename:
            _LOGGER.error("No map filename defined.")
            return
        map = await self.get(f"alms/{self._serial}/map")
        if map:
            with open(self.map_filename, "wb") as file:
                file.write(map)

    async def put_command(self, command: str):
        """Send a command to the mower.

        Args:
            command (str): command should be one of "mow", "pause", "returnToDock"

        Returns:
            str: either result of the call or 'Wrong Command'

        """
        if command in COMMANDS:
            return await self.put(f"alms/{self._serial}/state", {"state": command})
        _LOGGER.warning("%s not valid", command)
        return "Wrong Command!"

    async def put_mow_mode(self, command: typing.Any):
        """Set the mower to mode manual (false-ish) or predictive (true-ish).

        Args:
            command (str/bool): should be str that is bool-ish (true, True, false, False) or a bool.

        Returns:
            str: either result of the call or 'Wrong Command'
            
        """
        if command in ("true", "false", "True", "False") or isinstance(command, bool):
            return await self.put(
                f"alms/{self._serial}/predictive", {"enabled": command}
            )
        _LOGGER.warning("%s not valid", command)
        return "Wrong Command!"

    async def put_predictive_cal(self, calendar: dict = DEFAULT_CALENDAR):
        """Set the predictive calendar."""
        return await self.put(f"alms/{self._serial}/predictive/calendar", calendar)

    async def login(self, attempts=0):
        """Login to the api and store the context."""
        _LOGGER.debug("Logging in, attempt: %s", attempts)
        self._login(
            await self._request(
                method=Methods.POST,
                path="authenticate",
                data=DEFAULT_BODY,
                headers=DEFAULT_HEADER,
                auth=BasicAuth(self._username, self._password),
                timeout=30,
                attempts=attempts,
            )
        )

    async def _request(
        self,
        method: Methods,
        path: str,
        data: dict = None,
        headers=None,
        auth=None,
        timeout: int = 30,
        attempts: int = 0,
    ):
        """Send a request and return the response."""
        if attempts >= 3:
            _LOGGER.warning("Three or four attempts done, waiting 30 seconds")
            await asyncio.sleep(30)
        if attempts == 5:
            _LOGGER.warning("Five attempts done, please try again later")
            return None
        url = f"{self._api_url}{path}"
        if not headers:
            headers = DEFAULT_HEADER.copy()
            headers["x-im-context-id"] = self._contextid
        try:
            async with self._session.request(
                method=method.value,
                url=url,
                json=data,
                headers=headers,
                auth=auth,
                timeout=timeout,
            ) as response:
                status = response.status
                if status == 200:
                    if method == Methods.PUT:
                        return True
                    if response.content_type == CONTENT_TYPE_JSON:
                        return await response.json()
                    return await response.content.read()
                if status == 204:
                    _LOGGER.info("204: No content in response from server")
                    return None
                if status == 400:
                    _LOGGER.error(
                        "400: Bad Request: won't retry. Message: %s",
                        (await response.content.read()).decode("UTF-8"),
                    )
                    return None
                if status == 401:
                    _LOGGER.info("401: Unauthorized: logging in again")
                    await self.login()
                    return await self._request(
                        method=method,
                        path=path,
                        data=data,
                        timeout=timeout,
                        attempts=attempts + 1,
                    )
                if status == 403:
                    _LOGGER.error("403: Forbidden: won't retry")
                    return None
                if status == 405:
                    _LOGGER.error(
                        "405: Method not allowed: Get is used but not allowerd, try a different method for path %s, won't retry",
                        path,
                    )
                    return None
                if status == 500:
                    _LOGGER.info("500: Internal Server Error")
                    return None
                if status == 501:
                    _LOGGER.info("501: Not implemented yet")
                    return None
                if status == 504:
                    if url.find("longpoll=true") > 0:
                        _LOGGER.info("504: longpoll stopped, no updates")
                        return None
                response.raise_for_status()
        except (asyncio.TimeoutError, ServerTimeoutError, HTTPGatewayTimeout) as e:
            _LOGGER.error("%s: Timeout on Bosch servers, retrying", e)
            return await self._request(
                method=method,
                path=path,
                data=data,
                timeout=timeout,
                attempts=attempts + 1,
            )
        except (TooManyRedirects, ClientResponseError) as e:
            _LOGGER.error("%s: Failed to update Indego status", e)
            return None
        except asyncio.CancelledError:
            _LOGGER.debug("Task cancelled by task runner")
            return None
        except Exception as e:
            _LOGGER.error("Request to %s gave a unhandled error: %s", url, e)
            return None

    async def get(self, path: str, timeout: int = 30, attempts: int = 0):
        """Send a GET request and return the response as a dict."""
        return await self._request(
            method=Methods.GET, path=path, timeout=timeout, attempts=attempts
        )

    async def put(self, path: str, data: dict, timeout: int = 30):
        """Send a PUT request and return the response as a dict."""
        return await self._request(
            method=Methods.PUT, path=path, data=data, timeout=timeout
        )

