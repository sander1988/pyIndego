""" API for Bosch API server for Indego lawn mower """
import asyncio
import json
import logging
import typing

import aiohttp
import requests
from aiofile import AIOFile
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
    def __init__(
        self,
        username: str,
        password: str,
        serial: str,
        map_filename: str = None,
        api_url: str = DEFAULT_URL,
    ):
        super().__init__(username, password, serial, map_filename, api_url)
        self._session = aiohttp.ClientSession(raise_for_status=True)

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, type, value, traceback):
        await self.close()

    async def start(self):
        if not self._logged_in:
            await self.login()

    async def close(self):
        await self._session.close()

    async def update_all(self, force=False):
        await asyncio.gather(
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
            ]
        )

    async def update_generic_data(self):
        self._update_generic_data(await self.get(f"alms/{self._serial}"))

    async def update_alerts(self):
        self._update_alerts(await self.get("alerts"))

    async def update_last_completed_mow(self):
        self._update_last_completed_mow(
            await self.get(f"alms/{self._serial}/predictive/lastcutting")
        )

    async def update_location(self):
        self._update_location(
            await self.get(f"alms/{self._serial}/predictive/location")
        )

    async def update_next_mow(self):
        self._update_next_mow(
            await self.get(f"alms/{self._serial}/predictive/nextcutting")
        )

    async def update_operating_data(self):
        self._update_operating_data(
            await self.get(f"alms/{self._serial}/operatingData")
        )

    async def update_state(self, force=False, longpoll=False, longpoll_timeout=120):
        path = f"alms/{self._serial}/state"
        if longpoll:
            if self.state:
                last_state = self.state.state
            else:
                last_state = 0
            path = f"{path}?longpoll=true&timeout={longpoll_timeout}&last={last_state}"
        if force:
            path = f"{path}?forceRefresh=true"

        self._update_state(await self.get(path))

    async def update_updates_available(self):
        if self._online:
            self._update_updates_available(
                await self.get(f"alms/{self._serial}/updates")
            )

    async def update_users(self):
        self._update_users(await self.get(f"users/{self._userid}"))

    async def update_network(self):
        self._update_network(await self.get(f"alms/{self._serial}/network"))

    async def download_map(self, filename=None):
        if filename:
            self.map_filename = filename
        if not self.map_filename:
            _LOGGER.error("No map filename defined.")
            return
        async with AIOFile(self.map_filename, "wb") as afp:
            await afp.write(await self.get(f"alms/{self._serial}/map"))

    async def put_command(self, command: str):
        if command in COMMANDS:
            return await self.put(f"alms/{self._serial}/state", {"state": command})
        _LOGGER.warning("%s not valid", command)
        return "Wrong Command!"

    async def put_mow_mode(self, command: typing.Any):
        if command in ("true", "false", "True", "False") or isinstance(command, bool):
            return await self.put(
                f"alms/{self._serial}/predictive", {"enabled": command}
            )
        _LOGGER.warning("%s not valid", command)
        return "Wrong Command!"

    async def put_predictive_cal(self, calendar: dict = DEFAULT_CALENDAR):
        return await self.put(f"alms/{self._serial}/predictive/calendar", calendar)

    async def login(self):
        try:
            async with self._session.post(
                f"{self._api_url}authenticate",
                json=DEFAULT_BODY,
                headers=DEFAULT_HEADER,
                auth=BasicAuth(self._username, self._password),
                timeout=30,
            ) as self._login_session:
                self._login(await self._login_session.json())
        except ClientResponseError as e:
            _LOGGER.error("Invalid credentials: %s", e)

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
