"""Constants for pyIndego."""
from enum import Enum


class Methods(Enum):
    """Enum with HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


DEFAULT_URL = "https://api.indego.iot.bosch-si.com/api/v1/"
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE = "Content-Type"
DEFAULT_BODY = {
    "device": "",
    "os_type": "Android",
    "os_version": "4.0",
    "dvc_manuf": "unknown",
    "dvc_type": "unknown",
}
COMMANDS = ("mow", "pause", "returnToDock")

DEFAULT_HEADER = {CONTENT_TYPE: CONTENT_TYPE_JSON}
DEFAULT_LOOKUP_VALUE = "Not in database."

DEFAULT_CALENDAR = {
    "sel_cal": 1,
    "cals": [
        {
            "cal": 1,
            "days": [
                {
                    "day": 0,
                    "slots": [
                        {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0},
                        {"En": True, "StHr": 20, "StMin": 0, "EnHr": 23, "EnMin": 59},
                    ],
                },
                {
                    "day": 1,
                    "slots": [
                        {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0},
                        {"En": True, "StHr": 20, "StMin": 0, "EnHr": 23, "EnMin": 59},
                    ],
                },
                {
                    "day": 2,
                    "slots": [
                        {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0},
                        {"En": True, "StHr": 20, "StMin": 0, "EnHr": 23, "EnMin": 59},
                    ],
                },
                {
                    "day": 3,
                    "slots": [
                        {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0},
                        {"En": True, "StHr": 20, "StMin": 0, "EnHr": 23, "EnMin": 59},
                    ],
                },
                {
                    "day": 4,
                    "slots": [
                        {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0},
                        {"En": True, "StHr": 20, "StMin": 0, "EnHr": 23, "EnMin": 59},
                    ],
                },
                {
                    "day": 5,
                    "slots": [
                        {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0},
                        {"En": True, "StHr": 20, "StMin": 0, "EnHr": 23, "EnMin": 59},
                    ],
                },
                {
                    "day": 6,
                    "slots": [
                        {"En": True, "StHr": 0, "StMin": 0, "EnHr": 23, "EnMin": 59}
                    ],
                },
            ],
        }
    ],
}

MOWER_STATE_DESCRIPTION_DETAIL = {
    0: "Reading status",
    101: "Mower lifted",
    257: "Charging",
    258: "Docked",
    259: "Docked - Software update",
    260: "Charging",
    261: "Docked",
    262: "Docked - Loading map",
    263: "Docked - Saving map",
    266: "Docked - Leaving dock",
    512: "Mowing - Leaving dock",
    513: "Mowing",
    514: "Mowing - Relocalising",
    515: "Mowing - Loading map",
    516: "Mowing - Learning lawn",
    517: "Mowing - Paused",
    518: "Border cut",
    519: "Idle in lawn",
    520: "Mowing - Learning lawn paused",
    521: "Border cut",
    523: "Mowing - Spot mowing",
    524: "Mowing - Random",
    525: "Mowing - Random complete",
    768: "Returning to Dock",
    769: "Returning to Dock",
    770: "Returning to Dock",
    771: "Returning to Dock - Battery low",
    772: "Returning to dock - Calendar timeslot ended",
    773: "Returning to dock - Battery temp range",
    774: "Returning to dock - requested by user/app",
    775: "Returning to dock - Lawn complete",
    776: "Returning to dock - Relocalising",
    1005: "Connection to dockingstation failed",
    1025: "Diagnostic mode",
    1026: "End of life",
    1027: "Service Requesting Status",
    1038: "Mower immobilized",
    1281: "Software update",
    1537: "Stuck on lawn, help needed",
    64513: "Sleeping",
    99999: "Offline",
}


MOWER_STATE_DESCRIPTION = {
    0: "Docked",
    101: "Docked",
    257: "Docked",
    258: "Docked",
    259: "Docked",
    260: "Docked",
    261: "Docked",
    262: "Docked",
    263: "Docked",
    266: "Mowing",
    512: "Mowing",
    513: "Mowing",
    514: "Mowing",
    515: "Mowing",
    516: "Mowing",
    517: "Mowing",
    518: "Mowing",
    519: "Mowing",
    520: "Mowing",
    521: "Mowing",
    522: "Mowing",
    523: "Mowing",
    524: "Mowing",
    525: "Mowing",
    768: "Mowing",
    769: "Mowing",
    770: "Mowing",
    771: "Mowing",
    772: "Mowing",
    773: "Mowing",
    774: "Mowing",
    775: "Mowing",
    776: "Mowing",
    1005: "Mowing",
    1025: "Diagnostic mode",
    1026: "End of life",
    1027: "Service Requesting Status",
    1038: "Mower immobilized",
    1281: "Software update",
    1537: "Stuck",
    64513: "Docked",
    99999: "Offline",
}

MOWER_MODEL_DESCRIPTION = {
    "3600HA2300": "Indego 1000",
    "3600HA2301": "Indego 1200",
    "3600HA2302": "Indego 1100",
    "3600HA2303": "Indego 13C",
    "3600HA2304": "Indego 10C",
    "3600HB0100": "Indego 350",
    "3600HB0101": "Indego 400",
    "3600HB0102": "Indego S+ 350 1gen",
    "3600HB0103": "Indego S+ 400 1gen",
    "3600HB0105": "Indego S+ 350 2gen",
    "3600HB0106": "Indego S+ 400 2gen",
    "3600HB0301": "Indego M+ 700",
}

MOWER_MODEL_VOLTAGE = {
    "3600HA2300": {"min": "297", "max": "369"},  # Indego 1000
    "3600HA2301": {"min": "297", "max": "369"},  # Indego 1200
    "3600HA2302": {"min": "297", "max": "369"},  # Indego 1100
    "3600HA2303": {"min": "297", "max": "369"},  # Indego 13C
    "3600HA2304": {"min": "297", "max": "369"},  # Indego 10C
    "3600HB0100": {"min": "0", "max": "100"},  # Indego 350
    "3600HB0101": {"min": "0", "max": "100"},  # Indego 400
    "3600HB0102": {"min": "0", "max": "100"},  # Indego S+ 350
    "3600HB0103": {"min": "0", "max": "100"},  # Indego S+ 400
    "3600HB0105": {"min": "0", "max": "100"},  # Indego S+ 350
    "3600HB0106": {"min": "0", "max": "100"},  # Indego S+ 400
    "3600HB0301": {"min": "0", "max": "100"},  # Indego M+ 700
}

MOWING_MODE_DESCRIPTION = {
    "smart": "SmartMowing",
    "calendar": "Calendar",
    "manual": "Manual",
}

ALERT_ERROR_CODE = {
    "104": "Stop button pushed",
    "101": "Mower lifted",
    "115": "Mower is stuck",
    "149": "Mower outside perimeter cable",
    "151": "Perimeter cable signal missing",
    "ntfy_blade_life": "Reminder blade life",
}


DAY_MAPPING = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}
