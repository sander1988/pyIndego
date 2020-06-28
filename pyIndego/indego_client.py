"""API for Bosch API server for Indego lawn mower."""
import json
import logging
import typing
import time

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from requests.exceptions import RequestException
from requests.exceptions import Timeout
from requests.exceptions import TooManyRedirects

from . import __version__
from .const import Methods
from .const import COMMANDS
from .const import CONTENT_TYPE
from .const import CONTENT_TYPE_JSON
from .const import DEFAULT_BODY
from .const import DEFAULT_CALENDAR
from .const import DEFAULT_HEADER
from .const import DEFAULT_URL
from .indego_base_client import IndegoBaseClient

_LOGGER = logging.getLogger(__name__)


class IndegoClient(IndegoBaseClient):
    """Class for Indego Non-Async Client."""

    def __init__(
        self,
        username: str,
        password: str,
        serial: str,
        map_filename: str = None,
        api_url: str = DEFAULT_URL,
    ):
        """Initialize the Client.

        Args:
            username (str): username for Indego Account
            password (str): password for Indego Account
            serial (str): serial number of the mower
            map_filename (str, optional): Filename to store maps in. Defaults to None.
            api_url (str, optional): url for the api, defaults to DEFAULT_URL.

        """
        super().__init__(username, password, serial, map_filename, api_url)

    def __enter__(self):
        """Enter for with."""
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        """Exit for with."""
        pass

    def start(self):
        """Login if not done."""
        if not self._logged_in:
            self.login()

    def update_all(self, force=False):
        """Update all states."""
        self.update_generic_data()
        self.update_state(force)
        self.update_alerts()
        self.update_last_completed_mow()
        self.update_location()
        self.update_next_mow()
        self.update_operating_data()
        self.update_updates_available()
        self.update_users()
        self.update_network()

    def update_generic_data(self):
        """Update generic data."""
        self._update_generic_data(self.get(f"alms/{self._serial}"))

    def update_alerts(self):
        """Update alerts."""
        self._update_alerts(self.get("alerts"))

    def update_last_completed_mow(self):
        """Update last completed mow."""
        self._update_last_completed_mow(
            self.get(f"alms/{self._serial}/predictive/lastcutting")
        )

    def update_location(self):
        """Update location."""
        self._update_location(self.get(f"alms/{self._serial}/predictive/location"))

    def update_next_mow(self):
        """Update next mow datetime."""
        self._update_next_mow(self.get(f"alms/{self._serial}/predictive/nextcutting"))

    def update_operating_data(self):
        """Update operating data."""
        self._update_operating_data(self.get(f"alms/{self._serial}/operatingData"))

    def update_state(self, force=False, longpoll=False, longpoll_timeout=120):
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

        self._update_state(self.get(path, timeout=longpoll_timeout + 30))

    def update_updates_available(self):
        """Update updates available."""
        if self._online:
            self._update_updates_available(self.get(f"alms/{self._serial}/updates"))

    def update_users(self):
        """Update users."""
        self._update_users(self.get(f"users/{self._userid}"))

    def update_network(self):
        """Update network."""
        self._update_network(self.get(f"alms/{self._serial}/network"))

    def update_config(self):
        """Update config."""
        self._update_config(self.get(f"alms/{self._serial}/config"))

    def update_setup(self):
        """Update setup."""
        self._update_setup(self.get(f"alms/{self._serial}/setup"))

    def update_security(self):
        """Update security."""
        self._update_security(self.get(f"alms/{self._serial}/security"))

    def download_map(self, filename: str = None):
        """Download the map.

        Args:
            filename (str, optional): Filename for the map. Defaults to None, can also be filled by the filename set in init.

        """
        if filename:
            self.map_filename = filename
        if not self.map_filename:
            _LOGGER.error("No map filename defined.")
            return
        map = self.get(f"alms/{self._serial}/map")
        if map:
            with open(self.map_filename, "wb") as afp:
                afp.write(map)

    def put_command(self, command: str):
        """Send a command to the mower.

        Args:
            command (str): command should be one of "mow", "pause", "returnToDock"

        Returns:
            str: either result of the call or 'Wrong Command'

        """
        if command in COMMANDS:
            return self.put(f"alms/{self._serial}/state", {"state": command})
        _LOGGER.warning("%s not valid", command)
        return "Wrong Command!"

    def put_mow_mode(self, command: typing.Any):
        """Set the mower to mode manual (false-ish) or predictive (true-ish).

        Args:
            command (str/bool): should be str that is bool-ish (true, True, false, False) or a bool.

        Returns:
            str: either result of the call or 'Wrong Command'

        """
        if command in ("true", "false", "True", "False") or isinstance(command, bool):
            return self.put(f"alms/{self._serial}/predictive", {"enabled": command})
        _LOGGER.warning("%s not valid", command)
        return "Wrong Command!"

    def put_predictive_cal(self, calendar: dict = DEFAULT_CALENDAR):
        """Set the predictive calendar."""
        return self.put(f"alms/{self._serial}/predictive/calendar", calendar)

    def login(self, attempts=0):
        """Login to the api and store the context."""
        _LOGGER.debug("Logging in, attempt: %s", attempts)
        self._login(
            self._request(
                method=Methods.POST,
                path="authenticate",
                data=DEFAULT_BODY,
                headers=DEFAULT_HEADER,
                auth=HTTPBasicAuth(self._username, self._password),
                timeout=30,
                attempts=attempts,
            )
        )

    def _request(  # noqa: C901
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
            _LOGGER.warning("Three attempts done, waiting 30 seconds.")
            time.sleep(30)
        if attempts >= 5:
            _LOGGER.warning("Five attempts done, please try again manually.")
            return None
        url = f"{self._api_url}{path}"
        if not headers:
            headers = DEFAULT_HEADER.copy()
            headers["x-im-context-id"] = self._contextid
        try:
            response = requests.request(
                method=method.value,
                url=url,
                json=data,
                headers=headers,
                auth=auth,
                timeout=timeout,
            )
            status = response.status_code
            if status == 200:
                if method == Methods.PUT:
                    return True
                if CONTENT_TYPE_JSON in response.headers[CONTENT_TYPE].split(";"):
                    return response.json()
                else:
                    return response.content
            if status == 204:
                _LOGGER.info("204: No content in response from server")
                return None
            if status == 400:
                _LOGGER.error("400: Bad Request: won't retry.")
                return None
            if status == 401:
                _LOGGER.info("401: Unauthorized: logging in again.")
                self.login()
                return self._request(
                    method=method,
                    path=path,
                    data=data,
                    timeout=timeout,
                    attempts=attempts + 1,
                )
            if status == 403:
                _LOGGER.error("403: Forbidden: won't retry.")
                return None
            if status == 405:
                _LOGGER.error(
                    "405: Method not allowed: Get is used but not allowerd, try a different method for path %s, won't retry.",
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
                    _LOGGER.info("504: longpoll stopped, no updates.")
                    return None
            response.raise_for_status()
        except (Timeout) as e:
            _LOGGER.error("%s: Timeout on Bosch servers, retrying.", e)
            return self._request(
                method=method,
                path=path,
                data=data,
                timeout=timeout,
                attempts=attempts + 1,
            )
        except (TooManyRedirects, RequestException) as e:
            _LOGGER.error("%s: Failed to update Indego status.", e)
            return None
        except Exception as e:
            _LOGGER.error("Get gave a unhandled error: %s", e)
            return None

    def get(self, path: str, timeout: int = 30, attempts: int = 0):
        """Send a GET request and return the response as a dict."""
        return self._request(
            method=Methods.GET, path=path, timeout=timeout, attempts=attempts
        )

    def put(self, path: str, data: dict, timeout: int = 30):
        """Send a PUT request and return the response as a dict."""
        return self._request(method=Methods.PUT, path=path, data=data, timeout=timeout)
