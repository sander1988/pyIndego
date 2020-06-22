""" API for Bosch API server for Indego lawn mower """
import json
import logging
import typing

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from requests.exceptions import RequestException
from requests.exceptions import Timeout
from requests.exceptions import TooManyRedirects

from . import __version__
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
    def __init__(
        self,
        username: str,
        password: str,
        serial: str,
        map_filename: str = None,
        api_url: str = DEFAULT_URL,
    ):
        super().__init__(username, password, serial, map_filename, api_url)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        pass

    def start(self):
        if not self._logged_in:
            self.login()

    def update_all(self, force=False):
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
        self._update_generic_data(self.get(f"alms/{self._serial}"))

    def update_alerts(self):
        self._update_alerts(self.get("alerts"))

    def update_last_completed_mow(self):
        self._update_last_completed_mow(
            self.get(f"alms/{self._serial}/predictive/lastcutting")
        )

    def update_location(self):
        self._update_location(self.get(f"alms/{self._serial}/predictive/location"))

    def update_next_mow(self):
        self._update_next_mow(self.get(f"alms/{self._serial}/predictive/nextcutting"))

    def update_operating_data(self):
        self._update_operating_data(self.get(f"alms/{self._serial}/operatingData"))

    def update_state(self, force=False, longpoll=False, longpoll_timeout=120):
        path = f"alms/{self._serial}/state"
        #_LOGGER.debug("---Update State")
        if longpoll:
            if self.state:
                last_state = self.state.state
            else:
                last_state = 0
            path = f"{path}?longpoll=true&timeout={longpoll_timeout}&last={last_state}"
        if force:
            path = f"{path}?forceRefresh=true"

        self._update_state(self.get(path))

    def update_updates_available(self):
        if self._online:
            self._update_updates_available(self.get(f"alms/{self._serial}/updates"))

    def update_users(self):
        self._update_users(self.get(f"users/{self._userid}"))

    def update_network(self):
        self._update_network(self.get(f"alms/{self._serial}/network"))

    def download_map(self, filename=None):
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
        if command in COMMANDS:
            return self.put(f"alms/{self._serial}/state", {"state": command})
        _LOGGER.warning("%s not valid", command)
        return "Wrong Command!"

    def put_mow_mode(self, command: typing.Any):
        if command in ("true", "false", "True", "False") or isinstance(command, bool):
            return self.put(f"alms/{self._serial}/predictive", {"enabled": command})
        _LOGGER.warning("%s not valid", command)
        return "Wrong Command!"

    def put_predictive_cal(self, calendar: dict = DEFAULT_CALENDAR):
        return self.put(f"alms/{self._serial}/predictive/calendar", calendar)

    def login(self):
        response = requests.post(
            f"{self._api_url}authenticate",
            json=DEFAULT_BODY,
            headers=DEFAULT_HEADER,
            auth=HTTPBasicAuth(self._username, self._password),
            timeout=30,
        )
        try:
            response.raise_for_status()
        except HTTPError as e:
            _LOGGER.error("Invalid credentials: %s", e)
            return
        self._login(response.json())

    def get(self, path, timeout=30):
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
                response = requests.get(url, headers=headers, timeout=timeout)
                response.raise_for_status()
                if CONTENT_TYPE_JSON in response.headers[CONTENT_TYPE].split(";"):
                    return response.json()
                else:
                    return response.content
            except (Timeout, TooManyRedirects, RequestException) as e:
                _LOGGER.error("Failed to update Indego status. %s", e)
                return None
            except Exception as e:
                _LOGGER.error("Get gave a unhandled error: %s", e)
                return None
            else:
                _LOGGER.debug("      HTTP Status code: " + str(response.status_code))
                if response.status_code == 400:
                    _LOGGER.error("      server answer: Bad Request")
                    return None
                if response.status_code == 500:
                    #_LOGGER.error("      Server answer: Internal Server Error")
                    _LOGGER.info("      Server answer: Internal Server Error")
                    return None
                if response.status_code == 501:
                    #_LOGGER.error("      Server answer: not implemented yet")
                    _LOGGER.info("      Server answer: not implemented yet")
                    return None
                if response.status_code == 504:
                    _LOGGER.info("      Server backend did not have an update before timeout")
                    return None
                if response.status_code == 204:
                    _LOGGER.info("      No content in response from server")
                    return None
    
                elif response.status != 200:
                    # relogin for other codes
                    self.login()
                    headers["x-im-context-id"] = self._contextid
                    continue
                else:
                    _LOGGER.debug("      Json:" + str(response.json()))
                    response.raise_for_status()
                    _LOGGER.debug("   --- GET: end")
                    answer = True
                    return response.json()

        if attempts >= 5:
            _LOGGER.warning("Tried 5 times to get data but did not succeed")
            _LOGGER.warning(
                "Do you initilize with the correct username, password and serial?"
            )
            return None

    def put(self, path, data):
        """Send a PUT request and return the response as a dict."""
        headers = DEFAULT_HEADER.copy()
        headers["x-im-context-id"] = self._contextid

        full_url = self._api_url + path
        try:
            response = requests.put(full_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return True
        except (Timeout, TooManyRedirects, RequestException) as e:
            _LOGGER.error("Failed to update Indego status. %s", e)
            return None
        except Exception as e:
            _LOGGER.error("Get gave a unhandled error: %s", e)
            return None
