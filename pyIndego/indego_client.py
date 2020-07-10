"""API for Bosch API server for Indego lawn mower."""
import json
import logging
import time
import typing

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError, RequestException, Timeout, TooManyRedirects

from . import __version__
from .const import (
    COMMANDS,
    CONTENT_TYPE,
    CONTENT_TYPE_JSON,
    DEFAULT_BODY,
    DEFAULT_CALENDAR,
    DEFAULT_HEADER,
    DEFAULT_URL,
    Methods,
)
from .indego_base_client import IndegoBaseClient
from .states import Calendar

_LOGGER = logging.getLogger(__name__)


class IndegoClient(IndegoBaseClient):
    """Class for Indego Non-Async Client."""

    def __init__(
        self,
        username: str,
        password: str,
        serial: str = None,
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

    def delete_alert(self, alert_index: int):
        """Delete the alert with the specified index.

        Args:
            alert_index (int): index of alert to be deleted, should be in range or length of alerts.

        """
        if not self._alerts_loaded:
            raise ValueError("Alerts not loaded, please run update_alerts first.")
        alert_id = self._get_alert_by_index(alert_index)
        if alert_id:
            return self._request(Methods.DELETE, f"alerts/{alert_id}/")

    def delete_all_alerts(self):
        """Delete all the alerts."""
        if not self._alerts_loaded:
            raise ValueError("Alerts not loaded, please run update_alerts first.")
        if self.alerts_count > 0:
            return [
                self._request(Methods.DELETE, f"alerts/{alert.alert_id}")
                for alert in self.alerts
            ]
        _LOGGER.info("No alerts to delete")
        return None

    def download_map(self, filename: str = None):
        """Download the map.

        Args:
            filename (str, optional): Filename for the map. Defaults to None, can also be filled by the filename set in init.

        """
        if not self.serial:
            return
        if filename:
            self.map_filename = filename
        if not self.map_filename:
            raise ValueError("No map filename defined.")
        map = self.get(f"alms/{self.serial}/map")
        if map:
            with open(self.map_filename, "wb") as afp:
                afp.write(map)

    def put_alert_read(self, alert_index: int):
        """Set the alert to read.

        Args:
            alert_index (int): index of alert to be deleted, should be in range or length of alerts.

        """
        if not self._alerts_loaded:
            raise ValueError("Alerts not loaded, please run update_alerts first.")
        alert_id = self._get_alert_by_index(alert_index)
        if alert_id:
            return self._request(
                Methods.PUT, f"alerts/{alert_id}", data={"read_status": "read"}
            )

    def put_all_alerts_read(self):
        """Set to read the read_status of all alerts."""
        if not self._alerts_loaded:
            raise ValueError("Alerts not loaded, please run update_alerts first.")
        if self.alerts_count > 0:
            return [
                self._request(
                    Methods.PUT,
                    f"alerts/{alert.alert_id}",
                    data={"read_status": "read"},
                )
                for alert in self.alerts
            ]
        _LOGGER.warning("No alerts to set to read")
        return None

    def put_command(self, command: str):
        """Send a command to the mower.

        Args:
            command (str): command should be one of "mow", "pause", "returnToDock"

        Returns:
            str: either result of the call or 'Wrong Command'

        """
        if command in COMMANDS:
            if not self.serial:
                return
            return self.put(f"alms/{self.serial}/state", {"state": command})
        raise ValueError("Wrong Command, use one of 'mow', 'pause', 'returnToDock'")

    def put_mow_mode(self, command: typing.Any):
        """Set the mower to mode manual (false-ish) or predictive (true-ish).

        Args:
            command (str/bool): should be str that is bool-ish (true, True, false, False) or a bool.

        Returns:
            str: either result of the call or 'Wrong Command'

        """
        if command in ("true", "false", "True", "False") or isinstance(command, bool):
            if not self.serial:
                return
            return self.put(f"alms/{self.serial}/predictive", {"enabled": command})
        raise ValueError("Wrong Command, use True or False")

    def put_predictive_cal(self, calendar: dict = DEFAULT_CALENDAR):
        """Set the predictive calendar."""
        try:
            Calendar(**calendar["cals"][0])
        except TypeError as e:
            raise ValueError("Value for calendar is not valid: %s", e)
        if not self.serial:
            return
        return self.put(f"alms/{self.serial}/predictive/calendar", calendar)

    def update_alerts(self):
        """Update alerts."""
        self._update_alerts(self.get("alerts"))

    def update_all(self):
        """Update all states."""
        self.update_alerts()
        self.update_calendar()
        self.update_config()
        self.update_generic_data()
        self.update_last_completed_mow()
        self.update_location()
        self.update_network()
        self.update_next_mow()
        self.update_operating_data()
        self.update_predictive_calendar()
        self.update_predictive_schedule()
        self.update_security()
        self.update_setup()
        self.update_state()
        self.update_updates_available()
        self.update_user()

    def update_calendar(self):
        """Update calendar."""
        if not self.serial:
            return
        self._update_calendar(self.get(f"alms/{self.serial}/calendar"))

    def update_config(self):
        """Update config."""
        if not self.serial:
            return
        self._update_config(self.get(f"alms/{self.serial}/config"))

    def update_generic_data(self):
        """Update generic data."""
        if not self.serial:
            return
        self._update_generic_data(self.get(f"alms/{self.serial}"))

    def update_last_completed_mow(self):
        """Update last completed mow."""
        if not self.serial:
            return
        self._update_last_completed_mow(
            self.get(f"alms/{self.serial}/predictive/lastcutting")
        )

    def update_location(self):
        """Update location."""
        if not self.serial:
            return
        self._update_location(self.get(f"alms/{self.serial}/predictive/location"))

    def update_network(self):
        """Update network."""
        if not self.serial:
            return
        self._update_network(self.get(f"alms/{self.serial}/network"))

    def update_next_mow(self):
        """Update next mow datetime."""
        if not self.serial:
            return
        self._update_next_mow(self.get(f"alms/{self.serial}/predictive/nextcutting"))

    def update_operating_data(self):
        """Update operating data."""
        if not self.serial:
            return
        self._update_operating_data(self.get(f"alms/{self.serial}/operatingData"))

    def update_predictive_calendar(self):
        """Update predictive_calendar."""
        if not self.serial:
            return
        self._update_predictive_calendar(
            self.get(f"alms/{self.serial}/predictive/calendar")
        )

    def update_predictive_schedule(self):
        """Update predictive_schedule."""
        if not self.serial:
            return
        self._update_predictive_schedule(
            self.get(f"alms/{self.serial}/predictive/schedule")
        )

    def update_security(self):
        """Update security."""
        if not self.serial:
            return
        self._update_security(self.get(f"alms/{self.serial}/security"))

    def update_setup(self):
        """Update setup."""
        if not self.serial:
            return
        self._update_setup(self.get(f"alms/{self.serial}/setup"))

    def update_state(self, force=False, longpoll=False, longpoll_timeout=120):
        """Update state. Can be both forced and with longpoll.

        Args:
            force (bool, optional): Force the state refresh, wakes up the mower. Defaults to False.
            longpoll (bool, optional): Do a longpoll. Defaults to False.
            longpoll_timeout (int, optional): Timeout of the longpoll. Defaults to 120.

        """
        if not self.serial:
            return
        path = f"alms/{self.serial}/state"
        if longpoll:
            last_state = 0
            if self.state:
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
        if not self.serial:
            return
        if self._online:
            self._update_updates_available(self.get(f"alms/{self.serial}/updates"))

    def update_user(self):
        """Update users."""
        self._update_user(self.get(f"users/{self._userid}"))

    def login(self, attempts=0):
        """Login to the api and store the context."""
        response = self._request(
            method=Methods.POST,
            path="authenticate",
            data=DEFAULT_BODY,
            headers=DEFAULT_HEADER,
            auth=HTTPBasicAuth(self._username, self._password),
            timeout=30,
            attempts=attempts,
        )
        self._login(response)
        if response is not None:
            _LOGGER.debug("Logged in")
            if not self._serial:
                list_of_mowers = self.get("alms")
                self._serial = list_of_mowers[0].get("alm_sn")
                _LOGGER.debug("Serial added")
            return True
        return False

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
                if method in (Methods.DELETE, Methods.PATCH, Methods.PUT):
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
                if path == "authenticate":
                    _LOGGER.info(
                        "401: Unauthorized, credentials are wrong, won't retry"
                    )
                    return None
                _LOGGER.info("401: Unauthorized: logging in again")
                login_result = self.login()
                if login_result:
                    return self._request(
                        method=method,
                        path=path,
                        data=data,
                        timeout=timeout,
                        attempts=attempts + 1,
                    )
                return None
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

    def get(self, path: str, timeout: int = 30):
        """Send a GET request and return the response as a dict."""
        return self._request(method=Methods.GET, path=path, timeout=timeout)

    def put(self, path: str, data: dict, timeout: int = 30):
        """Send a PUT request and return the response as a dict."""
        return self._request(method=Methods.PUT, path=path, data=data, timeout=timeout)
