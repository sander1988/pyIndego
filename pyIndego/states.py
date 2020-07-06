"""Classes for states of pyIndego."""
import logging
from dataclasses import dataclass, field, is_dataclass
from datetime import date, datetime, time, timedelta
from typing import List

from .const import (
    ALERT_ERROR_CODE,
    DAY_MAPPING,
    DEFAULT_LOOKUP_VALUE,
    MOWER_MODEL_DESCRIPTION,
    MOWING_MODE_DESCRIPTION,
)
from .helpers import convert_bosch_datetime, nested_dataclass

_LOGGER = logging.getLogger(__name__)


@dataclass
class Alert:
    """Alert class."""

    alm_sn: str = field(repr=False, default=None)
    alert_id: str = None
    error_code: str = None
    headline: str = None
    date: datetime = None
    message: str = None
    read_status: str = None
    flag: str = None
    push: bool = None
    alert_description: str = None

    def __post_init__(self):
        """Set alert description."""
        self.alert_description = ALERT_ERROR_CODE.get(
            self.error_code, DEFAULT_LOOKUP_VALUE
        )
        self.date = convert_bosch_datetime(self.date)


@dataclass
class ModelVoltage:
    """Model voltage Class."""

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
    """Battery Class."""

    percent: int = None
    voltage: float = None
    cycles: int = None
    discharge: float = None
    ambient_temp: int = None
    battery_temp: int = None
    percent_adjusted: int = None

    def update_percent_adjusted(self, voltage: ModelVoltage):
        """Set percent adjusted."""
        if self.percent:
            self.percent_adjusted = round(
                (int(self.percent) - voltage.min) / ((voltage.max - voltage.min) / 100)
            )


@dataclass
class CalendarSlot:
    """Class for CalendarSlots."""

    En: bool = None
    StHr: int = None
    StMin: int = None
    EnHr: int = None
    EnMin: int = None
    Attr: str = None
    start: time = None
    end: time = None
    dt: datetime = None

    def __post_init__(self):
        """Convert start and end in time format."""
        if self.StHr is not None and self.StMin is not None:
            self.start = time(self.StHr, self.StMin)
        if self.EnHr is not None and self.EnMin is not None:
            self.end = time(self.EnHr, self.EnMin)


@nested_dataclass
class CalendarDay:
    """Class for CalendarDays."""

    day: int = None
    day_name: str = None
    slots: List[CalendarSlot] = field(default_factory=lambda: [CalendarSlot])

    def __post_init__(self):
        """Update the dayname."""
        if self.day is not None:
            self.day_name = DAY_MAPPING[self.day]
        if self.slots:
            for slot in self.slots:
                if slot.En:
                    today = date.today().weekday()
                    date_offset = timedelta(
                        days=self.day - today, hours=slot.StHr, minutes=slot.StMin
                    )
                    new_dt = (
                        datetime.now().replace(
                            hour=0, minute=0, second=0, microsecond=0
                        )
                        + date_offset
                    )
                    if new_dt.date() < date.today():
                        new_dt = new_dt + timedelta(days=7)
                    slot.dt = new_dt


@nested_dataclass
class Calendar:
    """Class for Calendar."""

    cal: int = None
    days: List[CalendarDay] = field(default_factory=lambda: [CalendarDay])


@nested_dataclass
class PredictiveSchedule:
    """Class for PredictiveSchedule."""

    schedule_days: List[CalendarDay] = field(default_factory=lambda: [CalendarDay])
    exclusion_days: List[CalendarDay] = field(default_factory=lambda: [CalendarDay])


@nested_dataclass
class GenericData:
    """Generic Data Class."""

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
        """Set model description, voltage, mode description."""
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
    """Location Class."""

    latitude: float = None
    longitude: float = None
    timezone: str = None


@dataclass
class Network:
    """Network Class."""

    mcc: int = None
    mnc: int = None
    rssi: int = None
    currMode: str = None
    configMode: str = None
    steeredRssi: int = None
    networkCount: int = None
    networks: List[int] = None


@dataclass
class Config:
    """Config Class."""

    region: int = None
    language: int = None
    border_cut: int = None
    is_pin_set: bool = None
    wire_id: int = None
    bump_sensitivity: int = None
    alarm_mode: bool = None


@dataclass
class Setup:
    """Setup Class."""

    hasOwner: bool = None
    hasPin: bool = None
    hasMap: bool = None
    hasAutoCal: bool = None
    hasIntegrityCheckPassed: bool = None


@dataclass
class Security:
    """Security Class."""

    enabled: bool = None
    autolock: bool = None


@dataclass
class RuntimeDetail:
    """Runtime Details Class."""

    operate: int = None
    charge: int = None
    cut: int = field(init=False, default=None)

    def update_cut(self):
        """Update cut."""
        self.cut = round(self.operate - self.charge)


@nested_dataclass
class Runtime:  # pylint: disable=no-member,assigning-non-slot
    """Runtime Class."""

    total: RuntimeDetail = field(default_factory=RuntimeDetail)
    session: RuntimeDetail = field(default_factory=RuntimeDetail)

    def __post_init__(self):
        """Set cuts and calc totals."""
        if self.total.charge:
            self.total.charge = round(self.total.charge / 100)
        if self.total.operate:
            self.total.operate = round(self.total.operate / 100)
        if self.total.charge:
            self.total.update_cut()
        if self.session.charge:
            self.session.update_cut()
        else:
            self.session.cut = 0


@dataclass
class Garden:
    """Garden Class."""

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
    """Operating Data Class."""

    hmiKeys: str = None
    battery: Battery = field(default_factory=Battery)
    garden: Garden = field(default_factory=Garden)
    runtime: Runtime = field(default_factory=Runtime)


@nested_dataclass
class State:
    """State Class."""

    state: int = None
    map_update_available: bool = None
    mowed: int = None
    mowmode: int = None
    error: int = None
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
class User:
    """User Class."""

    email: str = None
    display_name: str = None
    language: str = None
    country: str = None
    optIn: bool = None
    optInApp: bool = None
