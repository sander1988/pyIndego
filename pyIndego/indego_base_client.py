"""Base class for indego."""
import logging
import typing
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import replace

from .const import Methods
from .const import ALERT_ERROR_CODE
from .const import CONTENT_TYPE
from .const import CONTENT_TYPE_JSON
from .const import DEFAULT_BODY
from .const import DEFAULT_CALENDAR
from .const import DEFAULT_URL
from .const import MOWER_MODEL_DESCRIPTION
from .const import MOWER_MODEL_VOLTAGE
from .const import MOWER_STATE_DESCRIPTION
from .const import MOWER_STATE_DESCRIPTION_DETAIL
from .const import MOWING_MODE_DESCRIPTION
from .helpers import convert_bosch_datetime
from .states import Alerts
from .states import Battery
from .states import GenericData
from .states import Location
from .states import Network
from .states import Config
from .states import Setup
from .states import Security
from .states import OperatingData
from .states import Runtime
from .states import State
from .states import Users

_LOGGER = logging.getLogger(__name__)


class IndegoBaseClient(ABC):
    """Indego base client class."""

    def __init__(
        self,
        username: str,
        password: str,
        serial: str,
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
        self.generic_data = GenericData()
        self.operating_data = OperatingData()
        self.state = State()
        self.users = Users()
        self.network = Network()
        self.config = Config()
        self.setup = Setup()
        self.security = Security()
        self.battery = Battery()
        self.runtime = Runtime()
        self.location = Location()
        self.state_description = None
        self.state_description_detail = None
        self.last_completed_mow = None
        self.next_mow = None
        self.update_available = False
        self.alerts_count = 0

    @abstractmethod
    def update_all(self, force=False):
        """Update all states."""
        pass

    @abstractmethod
    def update_generic_data(self):
        """Update generic data."""
        pass

    def _update_generic_data(self, new):
        """Update generic data."""
        if new:
            self.generic_data = replace(self.generic_data, **new)
            self._update_battery_percentage_adjusted()

    @abstractmethod
    def update_alerts(self):
        """Update alerts."""
        pass

    def _update_alerts(self, new):
        """Update alerts."""
        if new:
            self.alerts = [Alerts(**a) for a in new]
            self.alerts_count = len(self.alerts)

    @abstractmethod
    def update_last_completed_mow(self):
        """Update last completed mow."""
        pass

    def _update_last_completed_mow(self, new):
        """Update last completed mow."""
        if new:
            self.last_completed_mow = convert_bosch_datetime(new["last_mowed"])

    @abstractmethod
    def update_location(self):
        """Update location."""
        pass

    def _update_location(self, new):
        """Update location."""
        if new:
            self.location = replace(self.location, **new)

    @abstractmethod
    def update_next_mow(self):
        """Update next mow datetime."""
        pass

    def _update_next_mow(self, new):
        """Update next mow datetime."""
        if new:
            self.next_mow = convert_bosch_datetime(new["mow_next"])

    @abstractmethod
    def update_operating_data(self):
        """Update operating data."""
        pass

    def _update_operating_data(self, new):
        """Update operating data."""
        if new:
            self._online = True
            self.operating_data = replace(self.operating_data, **new)
            self._update_battery_percentage_adjusted()
        else:
            self._online = False

    def _update_battery_percentage_adjusted(self):
        """Update the battery percentage adjusted field, relies on generic and operating data populated."""
        if (
            self.generic_data.model_voltage.min is not None
            and self.operating_data.battery.percent is not None
        ):
            self.operating_data.battery.update_percent_adjusted(
                self.generic_data.model_voltage
            )

    @abstractmethod
    def update_state(self, force=False, longpoll=False, longpoll_timeout=120):
        """Update state. Can be both forced and with longpoll.

        Args:
            force (bool, optional): Force the state refresh, wakes up the mower. Defaults to False.
            longpoll (bool, optional): Do a longpoll. Defaults to False.
            longpoll_timeout (int, optional): Timeout of the longpoll. Defaults to 120.

        """
        pass

    def _update_state(self, new):
        """Update state."""
        if new:
            self.state = replace(self.state, **new)
        self.state_description = MOWER_STATE_DESCRIPTION.get(str(self.state.state))
        self.state_description_detail = MOWER_STATE_DESCRIPTION_DETAIL.get(
            str(self.state.state)
        )

    @abstractmethod
    def update_updates_available(self):
        """Update updates available."""
        pass

    def _update_updates_available(self, new):
        """Update updates available."""
        _LOGGER.debug("Updates response: %s", new)
        if new:
            self.update_available = bool(new["available"])

    @abstractmethod
    def update_users(self):
        """Update users."""
        pass

    def _update_users(self, new):
        """Update users."""
        if new:
            self.users = replace(self.users, **new)

    @abstractmethod
    def update_network(self):
        """Update network."""
        pass

    def _update_network(self, new):
        """Update network."""
        if new:
            self.network = replace(self.network, **new)

    @abstractmethod
    def update_config(self):
        pass

    def _update_config(self, new):
        if new:
            self.config = replace(self.config, **new)

    @abstractmethod
    def update_setup(self):
        pass

    def _update_setup(self, new):
        if new:
            self.setup = replace(self.setup, **new)

    @abstractmethod
    def update_security(self):
        pass

    def _update_security(self, new):
        if new:
            self.security = replace(self.security, **new)

    @abstractmethod
    def download_map(self, filename=None):
        """Download the map.

        Args:
            filename (str, optional): Filename for the map. Defaults to None, can also be filled by the filename set in init.

        """
        pass

    @abstractmethod
    def put_command(self, command: str):
        """Send a command to the mower.

        Args:
            command (str): command should be one of "mow", "pause", "returnToDock"

        Returns:
            str: either result of the call or 'Wrong Command'

        """
        pass

    @abstractmethod
    def put_mow_mode(self, command: typing.Any):
        """Set the mower to mode manual (false-ish) or predictive (true-ish).

        Args:
            command (str/bool): should be str that is bool-ish (true, True, false, False) or a bool.

        Returns:
            str: either result of the call or 'Wrong Command'

        """
        pass

    @abstractmethod
    def put_predictive_cal(self, calendar: dict = DEFAULT_CALENDAR):
        """Set the predictive calendar."""
        pass

    @abstractmethod
    def login(self, attempts: int = 0):
        """Login to the Indego API."""
        pass

    def _login(self, login):
        """Login to the Indego API."""
        if login:
            _LOGGER.debug("---Call login")
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
        """Request implemented by the subclasses either synchronously or asynchronously.

        Args:
            method (Methods): HTTP method to be executed.
            path (str): url to call on top of base_url.
            data (dict, optional): if applicable, data to be sent, defaults to None.
            headers (dict, optional): headers to be included, defaults to None, which should be filled by the method.
            auth (BasicAuth or HTTPBasicAuth, optional): login specific attribute, defaults to None.
            timeout (int, optional): Timeout for the api call. Defaults to 30.
            attempts (int, optional): Number to keep track of retries, after three starts delaying, after five quites.

        """

    @abstractmethod
    def get(self, path: str, timeout: int):
        """Get implemented by the subclasses either synchronously or asynchronously.

        Args:
            path (str): url to call on top of base_url
            timeout (int, optional): Timeout for the api call. Defaults to 30.

        """
        pass

    @abstractmethod
    def put(self, path: str, data: dict, timeout: int):
        """Put implemented by the subclasses either synchronously or asynchronously.

        Args:
            path (str): url to call on top of base_url
            data (dict): data to put
            timeout (int, optional): Timeout for the api call. Defaults to 30.

        """
        pass

    def __repr__(self):
        """Create a string representing the mower."""
        return f"{self.generic_data.model_description} ({self.generic_data.alm_sn}) owned by {self.users.display_name}. {self.generic_data}, {self.state}, {self.operating_data}, last mowed: {self.last_completed_mow}, next mow: {self.next_mow}, {self.location}, {self.network}, {self.alerts}, map filename: {self.map_filename}, {self.runtime}, {self.battery}, update available: {self.update_available}, State Descr: {self.state_description}."
