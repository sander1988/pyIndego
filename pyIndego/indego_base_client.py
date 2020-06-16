"""Base class for indego."""
import logging
import typing
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import replace

from .const import ALERT_ERROR_CODE
from .const import CONTENT_TYPE
from .const import CONTENT_TYPE_JSON
from .const import DEFAULT_BODY
from .const import DEFAULT_CALENDAR
from .const import DEFAULT_URL
from .const import MOWER_MODEL_DESCRIPTION
from .const import MOWER_MODEL_VOLTAGE
from .const import MOWER_STATE_DESCRIPTION
from .const import MOWER_STATE_DESCRIPTION_DETAILED
from .const import MOWING_MODE_DESCRIPTION
from .helpers import convert_bosch_datetime
from .states import Alerts
from .states import Battery
from .states import GenericData
from .states import Location
from .states import Network
from .states import OperatingData
from .states import Runtime
from .states import State
from .states import Updates
from .states import Users

_LOGGER = logging.getLogger(__name__)


class IndegoBaseClient(ABC):
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
            username (str): Username for Indego
            password (str): Password for Indego
            serial (str): Serial number of the mower.

        """
        self._username = username
        self._password = password
        self._serial = serial
        self.map_filename = map_filename
        self._api_url = api_url
        self._logged_in = False
        self._online = False

        self.alerts = [Alerts()]
        self.generic_data = GenericData()
        self.operating_data = OperatingData()
        self.state = State()
        self.updates = Updates()
        self.users = Users()
        self.network = Network()
        self.battery = Battery()
        self.runtime = Runtime()
        self.location = Location()
        self.last_completed_mow = None
        self.next_mow = None
        self.update_available = None

    @abstractmethod
    def update_all(self, force=False):
        pass

    @abstractmethod
    def update_generic_data(self):
        pass

    def _update_generic_data(self, new):
        if new:
            self.generic_data = replace(self.generic_data, **new)
            self._update_battery_percentage_adjusted()

    @abstractmethod
    def update_alerts(self):
        pass

    def _update_alerts(self, new):
        if new:
            self.alerts = [Alerts(**a) for a in new]

    @abstractmethod
    def update_last_completed_mow(self):
        pass

    def _update_last_completed_mow(self, new):
        if new:
            self.last_completed_mow = convert_bosch_datetime(new["last_mowed"])

    @abstractmethod
    def update_location(self):
        pass

    def _update_location(self, new):
        if new:
            self.location = replace(self.location, **new)

    @abstractmethod
    def update_next_mow(self):
        pass

    def _update_next_mow(self, new):
        if new:
            self.next_mow = convert_bosch_datetime(new["mow_next"])

    @abstractmethod
    def update_operating_data(self):
        pass

    def _update_operating_data(self, new):
        if new:
            self._online = True
            self.operating_data = replace(self.operating_data, **new)
            self._update_battery_percentage_adjusted()
        else:
            self._online = False

    def _update_battery_percentage_adjusted(self):
        if (
            self.generic_data.model_voltage.min is not None
            and self.operating_data.battery.percent is not None
        ):
            self.operating_data.battery.update_percent_adjusted(
                self.generic_data.model_voltage
            )

    @abstractmethod
    def update_state(self, force=False, longpoll=False, longpoll_timeout=120):
        pass

    def _update_state(self, new):
        if new:
            self.state = replace(self.state, **new)

    @abstractmethod
    def update_updates_available(self):
        pass

    def _update_updates_available(self, new):
        if new:
            self.update_available = new["available"]

    @abstractmethod
    def update_users(self):
        pass

    def _update_users(self, new):
        if new:
            self.users = replace(self.users, **new)

    @abstractmethod
    def update_network(self):
        pass

    def _update_network(self, new):
        if new:
            self.network = replace(self.network, **new)

    @abstractmethod
    def download_map(self, filename=None):
        pass

    @abstractmethod
    def put_command(self, command: str):
        pass

    @abstractmethod
    def put_mow_mode(self, command: typing.Any):
        pass

    @abstractmethod
    def put_predictive_cal(self, calendar: dict = DEFAULT_CALENDAR):
        pass

    @abstractmethod
    def login(self):
        """Login to the Indego API."""
        pass

    def _login(self, login):
        if login:
            self._contextid = login["contextId"]
            self._userid = login["userId"]
            self._logged_in = True
        else:
            self._logged_in = False

    @abstractmethod
    def get(self, path: str, timeout: int = 30):
        """Get implemented by the subclasses either synchronously or asynchronously.

        Args:
            path (str): url to call on top of base_url
            timeout (int, optional): Timeout for the api call. Defaults to 30.
        
        """
        pass

    @abstractmethod
    def put(self, path: str, data: dict):
        """Put implemented by the subclasses either synchronously or asynchronously.

        Args:
            path (str): url to call on top of base_url
            data (dict): data to put
        
        """
        pass

    def __repr__(self):
        return f"{self.generic_data.model_description} ({self.generic_data.alm_sn}) owned by {self.users.display_name}. {self.generic_data}, {self.state}, {self.operating_data}, last mowed: {self.last_completed_mow}, next mow: {self.next_mow}, {self.location}, {self.network}, {self.alerts}, map filename: {self.map_filename}, {self.runtime}, {self.battery}, update available: {self.update_available}."
