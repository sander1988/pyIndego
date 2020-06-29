"""Classes for states of pyIndego."""
import logging
import typing
from dataclasses import dataclass
from dataclasses import field
from dataclasses import is_dataclass
from datetime import datetime

from .const import ALERT_ERROR_CODE
from .const import DEFAULT_LOOKUP_VALUE
from .const import MOWER_MODEL_DESCRIPTION
from .const import MOWING_MODE_DESCRIPTION
from .helpers import convert_bosch_datetime
from .helpers import nested_dataclass

_LOGGER = logging.getLogger(__name__)


@dataclass
class Alerts:
    alm_sn: str = field(repr=False, default=None)
    alert_id: str = None
    error_code: str = None
    headline: str = None
    date: datetime = field(default_factory=convert_bosch_datetime)
    message: str = None
    read_status: str = None
    flag: str = None
    push: bool = None
    alert_description: str = None

    def __post_init__(self):
        self.alert_description = ALERT_ERROR_CODE.get(
            self.error_code, DEFAULT_LOOKUP_VALUE
        )


@dataclass
class ModelVoltage:
    min: int = None
    max: int = None


MOWER_MODEL_VOLTAGE = {
    "3600HA2300": ModelVoltage(min=297, max=369),  # Indego 1000
    "3600HA2301": ModelVoltage(min=297, max=369),  # Indego 1200
    "3600HA2302": ModelVoltage(min=297, max=369),  # Indego 1100
    "3600HA2303": ModelVoltage(min=297, max=369),  # Indego 13C
    "3600HA2304": ModelVoltage(min=297, max=369),  # Indego 10C
    "3600HB0100": ModelVoltage(min=0, max=100),  # Indego 350
    "3600HB0101": ModelVoltage(min=0, max=100),  # Indego 400
    "3600HB0102": ModelVoltage(min=0, max=100),  # Indego S+ 350
    "3600HB0103": ModelVoltage(min=0, max=100),  # Indego S+ 400
    "3600HB0105": ModelVoltage(min=0, max=100),  # Indego S+ 350
    "3600HB0106": ModelVoltage(min=0, max=100),  # Indego S+ 400
    "3600HB0301": ModelVoltage(min=0, max=100)  # Indego M+ 700
    #    '3600HB0xxx': {'min': '0','max': '100'}   # Indego M+ 700
}


@dataclass
class Battery:
    percent: int = None
    voltage: float = None
    cycles: int = None
    discharge: float = None
    ambient_temp: int = None
    battery_temp: int = None
    percent_adjusted: int = None

    def update_percent_adjusted(self, voltage: ModelVoltage):
        if self.percent:
            self.percent_adjusted = round(
                (int(self.percent) - voltage.min) / ((voltage.max - voltage.min) / 100)
            )


@nested_dataclass
class GenericData:
    alm_name: str = None
    alm_sn: str = None
    service_counter: int = None
    needs_service: bool = None
    alm_mode: str = None
    bareToolnumber: str = None
    alm_firmware_version: str = None
    model_description: str = None
    model_voltage: ModelVoltage = field(default_factory=ModelVoltage)
    mowing_mode_description: str = None

    def __post_init__(self):
        self.model_description = MOWER_MODEL_DESCRIPTION.get(
            self.bareToolnumber, DEFAULT_LOOKUP_VALUE
        )
        self.model_voltage = MOWER_MODEL_VOLTAGE.get(
            self.bareToolnumber, ModelVoltage()
        )
        self.mowing_mode_description = MOWING_MODE_DESCRIPTION.get(
            self.alm_mode, DEFAULT_LOOKUP_VALUE
        )


@dataclass
class Location:
    latitude: float = None
    longitude: float = None
    timezone: str = None


@dataclass
class Network:
    mcc: int = None
    mnc: int = None
    rssi: int = None
    currMode: str = None
    configMode: str = None
    steeredRssi: int = None
    networkCount: int = None
    networks: typing.List[int] = None

@dataclass
class Config:
    region: int = None
    language: int = None
    border_cut: int = None
    is_pin_set: bool = None
    wire_id: int = None
    bump_sensitivity: int = None
    alarm_mode: bool = None

@dataclass
class Setup:
    hasOwner: bool = None
    hasPin: bool = None
    hasMap: bool = None
    hasAutoCal: bool = None
    hasIntegrityCheckPassed: bool = None

@dataclass
class Security:
    enabled: bool = None
    autolock: bool = None

@dataclass
class RuntimeDetail:
    operate: int = None
    charge: int = None
    cut: int = field(init=False, default=None)

    def update_cut(self):
        # _LOGGER.debug("---Update session cut")
        self.cut = round(self.operate - self.charge)
        # _LOGGER.debug(f"---self.cut = {self.cut}")


@nested_dataclass
class Runtime:
    total: RuntimeDetail = field(default_factory=RuntimeDetail)
    session: RuntimeDetail = field(default_factory=RuntimeDetail)

    def __post_init__(self):
        if self.total.charge:
            # _LOGGER.debug("---self.total.charge")
            self.total.charge = round(self.total.charge / 100)
        if self.total.operate:
            # _LOGGER.debug("---self.total.operate")
            self.total.operate = round(self.total.operate / 100)
        if self.total.charge:
            # _LOGGER.debug("---self.total.charge")
            self.total.update_cut()
        if self.session.charge:
            # _LOGGER.debug("---self.session.charge")
            self.session.update_cut()
        else:
            self.session.cut = 0


@dataclass
class Garden:
    id: int = None
    name: int = None
    signal_id: int = None
    size: int = None
    inner_bounds: int = None
    cuts: int = None
    runtime: int = None
    charge: int = None
    bumps: int = None
    stops: int = None
    last_mow: int = None
    map_cell_size: int = None


@nested_dataclass
class OperatingData:
    hmiKeys: str = None
    battery: Battery = field(default_factory=Battery)
    garden: Garden = field(default_factory=Garden)
    runtime: Runtime = field(default_factory=Runtime)


@nested_dataclass
class State:
    state: int = None
    map_update_available: bool = None
    mowed: int = None
    mowmode: int = None
    xPos: int = None
    yPos: int = None
    charge: int = None
    operate: int = None
    runtime: Runtime = field(default_factory=Runtime)
    mapsvgcache_ts: int = None
    svg_xPos: int = None
    svg_yPos: int = None
    config_change: bool = None
    mow_trig: bool = None


@dataclass
class Users:
    email: str = None
    display_name: str = None
    language: str = None
    country: str = None
    optIn: bool = None
    optInApp: bool = None
