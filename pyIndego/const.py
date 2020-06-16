

DEFAULT_URL = "https://api.indego.iot.bosch-si.com:443/api/v1/"
# CONST TAKEN FROM homeassistant.const
CONTENT_TYPE_JSON = "application/json"
# const taken from aiohttp.hdrs
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
                                {
                                    "En": True,
                                    "StHr": 0,
                                    "StMin": 0,
                                    "EnHr": 8,
                                    "EnMin": 0,
                                },
                                {
                                    "En": True,
                                    "StHr": 20,
                                    "StMin": 0,
                                    "EnHr": 23,
                                    "EnMin": 59,
                                },
                            ],
                        },
                        {
                            "day": 1,
                            "slots": [
                                {
                                    "En": True,
                                    "StHr": 0,
                                    "StMin": 0,
                                    "EnHr": 8,
                                    "EnMin": 0,
                                },
                                {
                                    "En": True,
                                    "StHr": 20,
                                    "StMin": 0,
                                    "EnHr": 23,
                                    "EnMin": 59,
                                },
                            ],
                        },
                        {
                            "day": 2,
                            "slots": [
                                {
                                    "En": True,
                                    "StHr": 0,
                                    "StMin": 0,
                                    "EnHr": 8,
                                    "EnMin": 0,
                                },
                                {
                                    "En": True,
                                    "StHr": 20,
                                    "StMin": 0,
                                    "EnHr": 23,
                                    "EnMin": 59,
                                },
                            ],
                        },
                        {
                            "day": 3,
                            "slots": [
                                {
                                    "En": True,
                                    "StHr": 0,
                                    "StMin": 0,
                                    "EnHr": 8,
                                    "EnMin": 0,
                                },
                                {
                                    "En": True,
                                    "StHr": 20,
                                    "StMin": 0,
                                    "EnHr": 23,
                                    "EnMin": 59,
                                },
                            ],
                        },
                        {
                            "day": 4,
                            "slots": [
                                {
                                    "En": True,
                                    "StHr": 0,
                                    "StMin": 0,
                                    "EnHr": 8,
                                    "EnMin": 0,
                                },
                                {
                                    "En": True,
                                    "StHr": 20,
                                    "StMin": 0,
                                    "EnHr": 23,
                                    "EnMin": 59,
                                },
                            ],
                        },
                        {
                            "day": 5,
                            "slots": [
                                {
                                    "En": True,
                                    "StHr": 0,
                                    "StMin": 0,
                                    "EnHr": 8,
                                    "EnMin": 0,
                                },
                                {
                                    "En": True,
                                    "StHr": 20,
                                    "StMin": 0,
                                    "EnHr": 23,
                                    "EnMin": 59,
                                },
                            ],
                        },
                        {
                            "day": 6,
                            "slots": [
                                {
                                    "En": True,
                                    "StHr": 0,
                                    "StMin": 0,
                                    "EnHr": 23,
                                    "EnMin": 59,
                                }
                            ],
                        },
                    ],
                }
            ],
        }

MOWER_STATE_DESCRIPTION_DETAILED = {
    "0": "Reading status",
    "257": "Charging",
    "258": "Docked",
    "259": "Docked - Software update",
    "260": "Docked",
    "261": "Docked",
    "262": "Docked - Loading map",
    "263": "Docked - Saving map",
    "513": "Mowing",
    "514": "Relocalising",
    "515": "Loading map",
    "516": "Learning lawn",
    "517": "Paused",
    "518": "Border cut",
    "519": "Idle in lawn",
    "769": "Returning to Dock",
    "770": "Returning to Dock",
    "771": "Returning to Dock - Battery low",
    "772": "Returning to dock - Calendar timeslot ended",
    "773": "Returning to dock - Battery temp range",
    "774": "Returning to dock - requested by user/app",
    "775": "Returning to dock - Lawn complete",
    "776": "Returning to dock - Relocalising",
    "1025": "Diagnostic mode",
    "1026": "End of life",
    "1281": "Software update",
    "1537": "Stuck on lawn, help needed",
    "64513": "Sleeping",
    "99999": "Offline",
    "None": "None",
}

MOWER_STATE_DESCRIPTION = {
    "0": "Docked",
    "257": "Docked",
    "258": "Docked",
    "259": "Docked",
    "260": "Docked",
    "261": "Docked",
    "262": "Docked",
    "263": "Docked",
    "513": "Mowing",
    "514": "Mowing",
    "515": "Mowing",
    "516": "Mowing",
    "517": "Mowing",
    "518": "Mowing",
    "519": "Mowing",
    "769": "Mowing",
    "770": "Mowing",
    "771": "Mowing",
    "772": "Mowing",
    "773": "Mowing",
    "774": "Mowing",
    "775": "Mowing",
    "776": "Mowing",
    "1025": "Diagnostic mode",
    "1026": "End of life",
    "1281": "Software update",
    "1537": "Stuck",
    "64513": "Docked",
    "99999": "Offline",
    "None": "None",
}


MOWER_MODEL_DESCRIPTION = {
    "3600HA2300": "Indego 1000",
    "3600HA2301": "Indego 1200",
    "3600HA2302": "Indego 1100",
    "3600HA2303": "Indego 13C",
    "3600HA2304": "Indego 10C",
    "3600HB0100": "Indego 350",
    "3600HB0101": "Indego 400",
    "3600HB0102": "Indego S+ 350",
    "3600HB0103": "Indego S+ 400",
    "3600HB0105": "Indego S+ 350 2020",
    "3600HB0106": "Indego S+ 400 2020",
    "3600HB0301": "Indego M+ 700"
    #    '3600HB0xxx': 'Indego M+ 700' missing model number
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
    "3600HB0301": {"min": "0", "max": "100"}  # Indego M+ 700
    #    '3600HB0xxx': {'min': '0','max': '100'}   # Indego M+ 700
}

MOWING_MODE_DESCRIPTION = {
    "smart": "SmartMowing",
    "calendar": "Calendar",
    "manual": "Manual",
}

ALERT_ERROR_CODE = {
    "104": "Stop button pushed",
    "115": "Mower is stuck",
    "149": "Mower uutside perimeter cable",
    "151": "Perimeter cable signal missing",
    "ntfy_blade_life": "Reminder blade life",
}
