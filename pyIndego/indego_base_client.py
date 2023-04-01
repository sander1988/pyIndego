"""Base class for indego."""
import logging
from abc import ABC, abstractmethod
from typing import Any, Optional, Callable, Awaitable

import pytz
import requests

from .const import (
    DEFAULT_CALENDAR,
    DEFAULT_LOOKUP_VALUE,
    DEFAULT_URL,
    MOWER_STATE_DESCRIPTION,
    MOWER_STATE_DESCRIPTION_DETAIL,
    Methods,
)
from .helpers import convert_bosch_datetime, generate_update
from .states import (
    Alert,
    Calendar,
    Config,
    GenericData,
    Location,
    Network,
    OperatingData,
    PredictiveSchedule,
    Security,
    Setup,
    State,
    User,
)

_LOGGER = logging.getLogger(__name__)


class IndegoBaseClient(ABC):
    """Indego base client class."""

    def __init__(
        self,
        token: str,
        token_refresh_method: Optional[Callable[[], Awaitable[str]]] = None,
        serial: str = None,
        map_filename: str = None,
        api_url: str = DEFAULT_URL,
        raise_request_exceptions: bool = False,
    ):
        """Abstract class for the Indego Clent, only use the Indego Client or Indego Async Client.

        Args:
            token (str): Bosch SingleKey ID OAuth token
            token_refresh_method (callback): Callback method to request an OAuth token refresh
            serial (str): serial number of the mower
            map_filename (str, optional): Filename to store maps in. Defaults to None.
            api_url (str, optional): url for the api, defaults to DEFAULT_URL.
            raise_request_exceptions (bool): Should unexpected API request exception be raised or not. Default False to keep things backwards compatible.
        """
        self._token = token
        self._token_refresh_method = token_refresh_method
        self._serial = serial
        self._mowers_in_account = None
        self.map_filename = map_filename
        self._api_url = api_url
        self._raise_request_exceptions = raise_request_exceptions
        self._logged_in = False
        self._online = False
        self._contextid = ""
        self._userid = None

        self.alerts = []
        self._alerts_loaded = False
        self.calendar = None
        self.config = None
        self.generic_data = None
        self.last_completed_mow = None
        self.location = None
        self.network = None
        self.next_mow = None
        self.operating_data = None
        self.predictive_calendar = None
        self.predictive_schedule = None
        self.security = None
        self.state = None
        self.setup = None
        self.runtime = None
        self.update_available = False
        self.user = None

    # Properties
    @property
    def serial(self):
        """Return the serial number of the mower."""
        if self._serial:
            return self._serial
        _LOGGER.warning("Serial not yet set, please login first")
        return None

    @property
    def mowers_in_account(self):
        """Return the list of mower detected during login."""
        return self._mowers_in_account

    @property
    def alerts_count(self):
        """Return the count of alerts."""
        if self.alerts:
            return len(self.alerts)
        return 0

    @property
    def state_description(self):
        """Return the description of the state."""
        if self.state:
            return MOWER_STATE_DESCRIPTION.get(self.state.state, DEFAULT_LOOKUP_VALUE)
        _LOGGER.warning("Please call update_state before calling this property")
        return None

    @property
    def state_description_detail(self):
        """Return the description detail of the state."""
        if self.state:
            return MOWER_STATE_DESCRIPTION_DETAIL.get(
                self.state.state, DEFAULT_LOOKUP_VALUE
            )
        _LOGGER.warning("Please call update_state before calling this property")
        return None

    @property
    def next_mows(self):
        """Return the next mows from the calendar without a timezone."""
        if self.calendar:
            return [
                slot.dt for day in self.calendar.days for slot in day.slots if slot.dt
            ]
        _LOGGER.warning("Please call update_calendar before calling this property")
        return None

    @property
    def next_mows_with_tz(self):
        """Return the next mows from the calendar with timezone from location."""
        if self.location and self.calendar:
            return [
                slot.dt.astimezone(pytz.timezone(self.location.timezone))
                for day in self.calendar.days
                for slot in day.slots
                if slot.dt
            ]
        if not self.location:
            _LOGGER.warning("Please call update_location before calling this property")
        if not self.calendar:
            _LOGGER.warning("Please call update_calendar before calling this property")
        return None

    # Methods
    @abstractmethod
    def delete_alert(self, alert_index: int):
        """Delete the alert with the specified index."""

    @abstractmethod
    def delete_all_alerts(self):
        """Delete all the alerts."""

    @abstractmethod
    def download_map(self, filename=None):
        """Download the map."""

    @abstractmethod
    def put_alert_read(self, alert_index: int):
        """Set to read the read_status of the alert with the specified index."""

    @abstractmethod
    def put_all_alerts_read(self):
        """Set to read the read_status of all alerts."""

    @abstractmethod
    def put_command(self, command: str):
        """Send a command to the mower."""

    @abstractmethod
    def put_mow_mode(self, command: Any):
        """Set the mower to mode manual (false-ish) or predictive (true-ish)."""

    @abstractmethod
    def put_predictive_cal(self, calendar: dict = DEFAULT_CALENDAR):
        """Set the predictive calendar."""

    @abstractmethod
    def update_alerts(self):
        """Update alerts."""

    @abstractmethod
    def get_alerts(self):
        """Update alerts and return them."""

    def _update_alerts(self, new):
        """Update alerts."""
        self._alerts_loaded = True
        if new:
            self.alerts = [Alert(**a) for a in new]
        else:
            self.alerts = []

    @abstractmethod
    def update_all(self):
        """Update all states."""

    @abstractmethod
    def update_calendar(self):
        """Update calendar."""

    @abstractmethod
    def get_calendar(self):
        """Update calendar and return it."""

    def _update_calendar(self, new):
        """Update calendar."""
        if new:
            self.calendar = generate_update(self.calendar, new["cals"][0], Calendar)

    @abstractmethod
    def update_config(self):
        """Update config."""

    @abstractmethod
    def get_config(self):
        """Update config and return it."""

    def _update_config(self, new):
        """Update config."""
        if new:
            self.config = generate_update(self.config, new, Config)

    @abstractmethod
    def update_generic_data(self):
        """Update generic data."""

    @abstractmethod
    def get_generic_data(self):
        """Update generic_data and return it."""

    def _update_generic_data(self, new):
        """Update generic data."""
        if new:
            self.generic_data = generate_update(self.generic_data, new, GenericData)
            self._update_battery_percentage_adjusted()

    @abstractmethod
    def update_last_completed_mow(self):
        """Update last completed mow."""

    @abstractmethod
    def get_last_completed_mow(self):
        """Update last_completed_mow and return it."""

    def _update_last_completed_mow(self, new):
        """Update last completed mow."""
        if new:
            self.last_completed_mow = convert_bosch_datetime(new["last_mowed"])

    @abstractmethod
    def update_location(self):
        """Update location."""

    @abstractmethod
    def get_location(self):
        """Update location and return it."""

    def _update_location(self, new):
        """Update location."""
        if new:
            self.location = generate_update(self.location, new, Location)

    @abstractmethod
    def update_network(self):
        """Update network."""

    @abstractmethod
    def get_network(self):
        """Update network and return it."""

    def _update_network(self, new):
        """Update network."""
        if new:
            self.network = generate_update(self.network, new, Network)

    @abstractmethod
    def update_next_mow(self):
        """Update next mow datetime."""

    @abstractmethod
    def get_next_mow(self):
        """Update next_mow and return it."""

    def _update_next_mow(self, new):
        """Update next mow datetime."""
        if new:
            self.next_mow = convert_bosch_datetime(new["mow_next"])

    @abstractmethod
    def update_operating_data(self):
        """Update operating data."""

    @abstractmethod
    def get_operating_data(self):
        """Update operating_data and return it."""

    def _update_operating_data(self, new):
        """Update operating data."""
        if new:
            self.operating_data = generate_update(
                self.operating_data, new, OperatingData
            )
            self._update_battery_percentage_adjusted()
            self._online = True
        else:
            self._online = False

    @abstractmethod
    def update_predictive_calendar(self):
        """Update predictive_calendar."""

    @abstractmethod
    def get_predictive_calendar(self):
        """Update predictive_calendar and return it."""

    def _update_predictive_calendar(self, new):
        """Update predictive_calendar."""
        if new:
            self.predictive_calendar = generate_update(
                self.predictive_calendar, new["cals"][0], Calendar
            )

    @abstractmethod
    def update_predictive_schedule(self):
        """Update predictive schedule."""

    @abstractmethod
    def get_predictive_schedule(self):
        """Update predictive_schedule and return it."""

    def _update_predictive_schedule(self, new):
        """Update predictive schedule."""
        if new:
            self.predictive_schedule = generate_update(
                self.predictive_schedule, new, PredictiveSchedule
            )

    @abstractmethod
    def update_security(self):
        """Update security."""

    @abstractmethod
    def get_security(self):
        """Update security and return it."""

    def _update_security(self, new):
        """Update security."""
        if new:
            self.security = generate_update(self.security, new, Security)

    @abstractmethod
    def update_setup(self):
        """Update setup."""

    @abstractmethod
    def get_setup(self):
        """Update setup and return it."""

    def _update_setup(self, new):
        """Update setup."""
        if new:
            self.setup = generate_update(self.setup, new, Setup)

    @abstractmethod
    def update_state(self, force=False, longpoll=False, longpoll_timeout=120):
        """Update state. Can be both forced and with longpoll."""

    @abstractmethod
    def get_state(self, force=False, longpoll=False, longpoll_timeout=120):
        """Update state and return it."""

    def _update_state(self, new):
        """Update state."""
        if new:
            self.state = generate_update(self.state, new, State)

    @abstractmethod
    def update_updates_available(self):
        """Update updates available."""

    @abstractmethod
    def get_updates_available(self):
        """Update updates_available and return it."""

    def _update_updates_available(self, new):
        """Update updates available."""
        if new:
            self.update_available = bool(new["available"])

    @abstractmethod
    def update_user(self):
        """Update users."""

    @abstractmethod
    def get_user(self):
        """Update user and return it."""

    def _update_user(self, new):
        """Update users."""
        if new:
            self.user = generate_update(self.user, new, User)

    @abstractmethod
    def _request(
        self,
        method: Methods,
        path: str,
        data: dict = None,
        headers: dict = None,
        timeout: int = 30,
        attempts: int = 0,
    ):
        """Request implemented by the subclasses either synchronously or asynchronously."""

    def _log_request_result(self, status: int, url: str) -> bool:
        """Log the API request result for certain status codes."""
        """Return False if the status is fatal and should be raised."""

        if status == 204:
            _LOGGER.debug("204: No content in response from server, ignoring")
            return True

        if status == 504 and url.find("longpoll=true") > 0:
            _LOGGER.debug("504: longpoll stopped, no updates")
            return True

        if 400 <= status < 600:
            _LOGGER.error("Request to '%s' failed with HTTP status code: %i", url, status)
            return not self._raise_request_exceptions

        return False

    @abstractmethod
    def get(self, path: str, timeout: int):
        """Get implemented by the subclasses either synchronously or asynchronously."""

    @abstractmethod
    def put(self, path: str, data: dict, timeout: int):
        """Put implemented by the subclasses either synchronously or asynchronously."""

    # internal methods
    def _get_alert_by_index(self, alert_index: int) -> int:
        """Return the alert_id based on index."""
        if not self._alerts_loaded:
            raise ValueError("Alerts not loaded, please run update_alerts first.")
        if self.alerts_count == 0:
            _LOGGER.info("No alerts to get")
            return None
        try:
            return self.alerts[alert_index].alert_id
        except IndexError as exc:
            raise IndexError(
                f"Wrong index for the alert, there are {self.alerts_count} alerts, so the highest index is: {self.alerts_count - 1}, supplied was {alert_index}"
            ) from exc

    def _update_battery_percentage_adjusted(self):
        """Update the battery percentage adjusted field, relies on generic and operating data populated."""
        if self.generic_data and self.operating_data:
            self.operating_data.battery.update_percent_adjusted(
                self.generic_data.model_voltage
            )

    def __repr__(self):
        """Create a string representing the mower."""
        str1 = (
            f"{self.generic_data.model_description} ({self.generic_data.alm_sn})"
            if self.generic_data
            else f"Indego mower"
        )
        str2 = f" owned by {self.user.display_name}." if self.user else f"."
        str3 = f" {self.generic_data}, " if self.generic_data else ""
        str4 = f" {self.state}, " if self.state else ""
        str5 = f" {self.operating_data}, " if self.operating_data else ""
        str6 = f", last mowed: {self.last_completed_mow}, next mow: {self.next_mow}, {self.location}, {self.network}, {self.alerts}, map filename: {self.map_filename}, {self.runtime}"
        str7 = f"{self.operating_data.battery} " if self.operating_data else ""
        str8 = f"update available: {self.update_available}, State Descr: {self.state_description}."
        return f"{str1}{str2}{str3}{str4}{str5}{str6}{str7}{str8}"
