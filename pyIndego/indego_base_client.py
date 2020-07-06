"""Base class for indego."""
import logging
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass, replace

from .const import (
    Methods,
    CONTENT_TYPE,
    CONTENT_TYPE_JSON,
    DEFAULT_BODY,
    DEFAULT_CALENDAR,
    DEFAULT_LOOKUP_VALUE,
    DEFAULT_URL,
    MOWER_MODEL_DESCRIPTION,
    MOWER_MODEL_VOLTAGE,
    MOWER_STATE_DESCRIPTION,
    MOWER_STATE_DESCRIPTION_DETAIL,
    MOWING_MODE_DESCRIPTION,
)
from .helpers import convert_bosch_datetime
from .states import (
    Alerts,
    Calendar,
    Battery,
    GenericData,
    Location,
    Network,
    Config,
    Setup,
    Security,
    OperatingData,
    PredictiveCalendar,
    PredictiveSchedule,
    Runtime,
    State,
    Users,
)

_LOGGER = logging.getLogger(__name__)


class IndegoBaseClient(ABC):
    """Indego base client class."""

    def __init__(
        self,
        username: str,
        password: str,
        serial: str = None,
        map_filename: str = None,
        api_url: str = DEFAULT_URL,
    ):
        """Abstract class for the Indego Clent, only use the Indego Client or Indego Async Client.

        Args:
            username (str): username for Indego Account
            password (str): password for Indego Account
            serial (str): serial number of the mower
            map_filename (str, optional): Filename to store maps in. Defaults to None.
            api_url (str, optional): url for the api, defaults to DEFAULT_URL.

        """
        self._username = username
        self._password = password
        self._serial = serial
        self.map_filename = map_filename
        self._api_url = api_url
        self._logged_in = False
        self._online = False
        self._contextid = ""

        self.alerts = [Alerts()]
        self.alerts_count = 0
        self.battery = Battery()
        self.calendar = Calendar()
        self.config = Config()
        self.generic_data = GenericData()
        self.last_completed_mow = None
        self.location = Location()
        self.network = Network()
        self.next_mow = None
        self.operating_data = OperatingData()
        self.predictive_calendar = PredictiveCalendar()
        self.predictive_schedule = PredictiveSchedule()
        self.security = Security()
        self.state = State()
        self.setup = Setup()
        self.runtime = Runtime()
        self.update_available = False
        self.users = Users()

    # Properties
    @property
    def serial(self):
        """Return the serial number of the mower."""
        if self._serial:
            return self._serial
        _LOGGER.warning("Serial not yet set, please login first")
        return None

    @property
    def state_description(self):
        """Return the description of the state."""
        return MOWER_STATE_DESCRIPTION.get(self.state.state, DEFAULT_LOOKUP_VALUE)

    @property
    def state_description_detail(self):
        """Return the description detail of the state."""
        return MOWER_STATE_DESCRIPTION_DETAIL.get(
            self.state.state, DEFAULT_LOOKUP_VALUE
        )

    # Methods
    @abstractmethod
    def delete_alert(self, alert_index: int):
        """Delete the alert with the specified index."""

    @abstractmethod
    def download_map(self, filename=None):
        """Download the map."""

    @abstractmethod
    def patch_alert_read(self, alert_index: int, read_status: bool):
        """Patch the read_status of the alert with the specified index."""

    @abstractmethod
    def put_command(self, command: str):
        """Send a command to the mower."""

    @abstractmethod
    def put_mow_mode(self, command: typing.Any):
        """Set the mower to mode manual (false-ish) or predictive (true-ish)."""

    @abstractmethod
    def put_predictive_cal(self, calendar: dict = DEFAULT_CALENDAR):
        """Set the predictive calendar."""

    @abstractmethod
    def update_alerts(self):
        """Update alerts."""

    def _update_alerts(self, new):
        """Update alerts."""
        if new:
            self.alerts = [Alerts(**a) for a in new]
            self.alerts_count = len(self.alerts)
        else:
            self.alerts = [Alerts()]
            self.alerts_count = 0

    @abstractmethod
    def update_all(self):
        """Update all states."""

    @abstractmethod
    def update_calendar(self):
        """Update calendar."""

    def _update_calendar(self, new):
        """Update calendar."""
        if new:
            self.calendar = replace(self.calendar, **new["cals"][0])

    @abstractmethod
    def update_config(self):
        """Update config."""

    def _update_config(self, new):
        """Update config."""
        if new:
            self.config = replace(self.config, **new)

    @abstractmethod
    def update_generic_data(self):
        """Update generic data."""

    def _update_generic_data(self, new):
        """Update generic data."""
        if new:
            self.generic_data = replace(self.generic_data, **new)
            self._update_battery_percentage_adjusted()

    @abstractmethod
    def update_last_completed_mow(self):
        """Update last completed mow."""

    def _update_last_completed_mow(self, new):
        """Update last completed mow."""
        if new:
            self.last_completed_mow = convert_bosch_datetime(new["last_mowed"])

    @abstractmethod
    def update_location(self):
        """Update location."""

    def _update_location(self, new):
        """Update location."""
        if new:
            self.location = replace(self.location, **new)

    @abstractmethod
    def update_network(self):
        """Update network."""

    def _update_network(self, new):
        """Update network."""
        if new:
            self.network = replace(self.network, **new)

    @abstractmethod
    def update_next_mow(self):
        """Update next mow datetime."""

    def _update_next_mow(self, new):
        """Update next mow datetime."""
        if new:
            self.next_mow = convert_bosch_datetime(new["mow_next"])

    @abstractmethod
    def update_operating_data(self):
        """Update operating data."""

    def _update_operating_data(self, new):
        """Update operating data."""
        if new:
            self.operating_data = replace(self.operating_data, **new)
            self._update_battery_percentage_adjusted()
            self._online = True
        else:
            self._online = False

    @abstractmethod
    def update_predictive_calendar(self):
        """Update predictive_calendar."""

    def _update_predictive_calendar(self, new):
        """Update predictive_calendar."""
        if new:
            self.predictive_calendar = replace(self.predictive_calendar, **new["cals"][0])

    @abstractmethod
    def update_predictive_schedule(self):
        """Update predictive schedule."""

    def _update_predictive_schedule(self, new):
        """Update predictive schedule."""
        if new:
            self.predictive_schedule = replace(self.predictive_schedule, **new)

    @abstractmethod
    def update_security(self):
        """Update security."""

    def _update_security(self, new):
        """Update security."""
        if new:
            self.security = replace(self.security, **new)

    @abstractmethod
    def update_setup(self):
        """Update setup."""

    def _update_setup(self, new):
        """Update setup."""
        if new:
            self.setup = replace(self.setup, **new)

    @abstractmethod
    def update_state(self, force=False, longpoll=False, longpoll_timeout=120):
        """Update state. Can be both forced and with longpoll."""

    def _update_state(self, new):
        """Update state."""
        if new:
            self.state = replace(self.state, **new)

    @abstractmethod
    def update_updates_available(self):
        """Update updates available."""

    def _update_updates_available(self, new):
        """Update updates available."""
        _LOGGER.debug("Updates response: %s", new)
        if new:
            self.update_available = bool(new["available"])

    @abstractmethod
    def update_users(self):
        """Update users."""

    def _update_users(self, new):
        """Update users."""
        if new:
            self.users = replace(self.users, **new)

    @abstractmethod
    def login(self, attempts: int = 0):
        """Login to the Indego API."""

    def _login(self, login):
        """Login to the Indego API."""
        if login:
            self._contextid = login["contextId"]
            self._userid = login["userId"]
            self._logged_in = True
        else:
            self._logged_in = False

    @abstractmethod
    def _request(
        self,
        method: Methods,
        path: str,
        data: dict = None,
        headers: dict = None,
        auth: typing.Any = None,
        timeout: int = 30,
        attempts: int = 0,
    ):
        """Request implemented by the subclasses either synchronously or asynchronously."""

    @abstractmethod
    def get(self, path: str, timeout: int):
        """Get implemented by the subclasses either synchronously or asynchronously."""

    @abstractmethod
    def post(self, path: str, timeout: int):
        """Post implemented by the subclasses either synchronously or asynchronously."""

    @abstractmethod
    def put(self, path: str, data: dict, timeout: int):
        """Put implemented by the subclasses either synchronously or asynchronously."""

    # internal methods
    def _get_alert_by_index(self, alert_index: int) -> int:
        """Return the alert_id based on index."""
        if 0 <= alert_index < self.alerts_count:
            _LOGGER.warning(
                "No alerts to patch, or alerts not loaded yet, use update_alerts first"
            )
            return None
        return self.alerts[alert_index].alert_id

    def _update_battery_percentage_adjusted(self):
        """Update the battery percentage adjusted field, relies on generic and operating data populated."""
        if (
            self.generic_data.model_voltage.min is not None
            and self.operating_data.battery.percent is not None
        ):
            self.operating_data.battery.update_percent_adjusted(
                self.generic_data.model_voltage
            )

    def __repr__(self):
        """Create a string representing the mower."""
        return f"{self.generic_data.model_description} ({self.generic_data.alm_sn}) owned by {self.users.display_name}. {self.generic_data}, {self.state}, {self.operating_data}, last mowed: {self.last_completed_mow}, next mow: {self.next_mow}, {self.location}, {self.network}, {self.alerts}, map filename: {self.map_filename}, {self.runtime}, {self.battery}, update available: {self.update_available}, State Descr: {self.state_description}."
