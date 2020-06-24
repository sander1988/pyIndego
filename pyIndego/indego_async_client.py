""" API for Bosch API server for Indego lawn mower """
import asyncio
import json
import logging
import typing

import aiohttp
import requests

# from aiofile import AIOFile
from aiohttp import ClientResponseError
from aiohttp import ServerTimeoutError
from aiohttp import TooManyRedirects
from aiohttp.helpers import BasicAuth

from . import __version__
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
        self._session = aiohttp.ClientSession(raise_for_status=True)

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
            if self.state:
                last_state = self.state.state
            else:
                last_state = 0
            path = f"{path}?longpoll=true&timeout={longpoll_timeout}&last={last_state}"
        if force:
            if longpoll:
                path = f"{path}&forceRefresh=true"
            else:
                path = f"{path}?forceRefresh=true"

        self._update_state(await self.get(path))

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
        # async with AIOFile(self.map_filename, "wb") as afp:
        #    await afp.write(await self.get(f"alms/{self._serial}/map"))
        map = self.get(f"alms/{self._serial}/map")
        if map:
            with open(self.map_filename, "wb") as afp:
                afp.write(map)

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

    async def login(self):
        """Login to the api and store the context."""
        async with self._session.post(
            f"{self._api_url}authenticate",
            json=DEFAULT_BODY,
            headers=DEFAULT_HEADER,
            auth=BasicAuth(self._username, self._password),
            timeout=30,
        ) as self._login_session:
            self._login(await self._login_session.json())

    async def get(self, path, timeout=30):
        """Send a GET request and return the response as a dict."""
        if not self._logged_in:
            _LOGGER.warning("Please log in before calling updates.")
            return None
        url = self._api_url + path
        headers = DEFAULT_HEADER.copy()
        headers["x-im-context-id"] = self._contextid

        attempts = 0
        while attempts < 5:
            attempts = attempts + 1
            try:
                async with self._session.get(
                    url, headers=headers, timeout=timeout
                ) as response:
                    if response.content_type == CONTENT_TYPE_JSON:
                        return await response.json()
                    else:
                        return await response.content.read()
            except (ServerTimeoutError, TooManyRedirects, ClientResponseError) as e:
                _LOGGER.error("Failed to update Indego status. %s", e)
                return None
            except Exception as e:
                _LOGGER.error("Get gave a unhandled error: %s", e)
                return None

            if response.status == 504:
                _LOGGER.error("Server backend did not have an update before timeout")
                return None
            elif response.status != 200:
                # relogin for other codes
                await self.login()
                headers["x-im-context-id"] = self._contextid
                continue

        if attempts >= 5:
            _LOGGER.warning("Tried 5 times to get data but did not succeed")
            _LOGGER.warning(
                "Do you initilize with the correct username, password and serial?"
            )
            return None

    async def put(self, path, data):
        """Send a PUT request and return the response as a dict."""
        headers = DEFAULT_HEADER.copy()
        headers["x-im-context-id"] = self._contextid

        full_url = self._api_url + path
        try:
            async with self._session.put(
                full_url, headers=headers, json=data, timeout=30
            ):
                return True
        except (ServerTimeoutError, TooManyRedirects, ClientResponseError) as e:
            _LOGGER.error("Failed to update Indego status. %s", e)
            return None
        except Exception as e:
            _LOGGER.error("Get gave a unhandled error: %s", e)
            return None
