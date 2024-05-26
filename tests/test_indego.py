"""Test the states of pyIndego."""
import asyncio
import logging
from datetime import datetime
from socket import error as SocketError
from typing import Final

import pytest
from aiohttp import (
    ClientOSError,
    ClientResponseError,
    ServerTimeoutError,
    TooManyRedirects,
)
from aiohttp.web_exceptions import HTTPGatewayTimeout
from mock import MagicMock, patch
from requests.exceptions import RequestException, Timeout
from requests.exceptions import TooManyRedirects as reqTooManyRedirects

from pyIndego import IndegoAsyncClient, IndegoClient
from pyIndego.const import CONTENT_TYPE, CONTENT_TYPE_JSON, Methods
from pyIndego.helpers import convert_bosch_datetime
from pyIndego.states import (
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

# region Test data
ALERT_RESPONSE: Final = {
    "alm_sn": "test_sn",
    "alert_id": "5efda84ffbf591182723be89",
    "error_code": "104",
    "headline": "Mower requires attention.",
    "date": "2020-07-02T09:26:39.589Z",
    "message": "Stop button activated. The Stop button has been activated. Please follow the instructions on the mower display.",
    "read_status": "read",
    "flag": "warning",
    "push": True,
}

CALENDAR_RESPONSE = {
    "cal": 3,
    "days": [
        {
            "day": 0,
            "slots": [
                {"En": True, "StHr": 10, "StMin": 0, "EnHr": 13, "EnMin": 0},
                {"En": False},
            ],
        },
        {
            "day": 2,
            "slots": [
                {"En": True, "StHr": 11, "StMin": 0, "EnHr": 14, "EnMin": 0},
                {"En": False},
            ],
        },
        {
            "day": 4,
            "slots": [
                {"En": True, "StHr": 10, "StMin": 0, "EnHr": 13, "EnMin": 0},
                {"En": False},
            ],
        },
    ],
}

SETUP_RESPONSE: Final = {
    "hasOwner": True,
    "hasPin": True,
    "hasMap": True,
    "hasAutoCal": False,
    "hasIntegrityCheckPassed": True,
}

LOCATION_RESPONSE: Final = {
    "latitude": "1.1234",
    "longitude": "1.1234",
    "timezone": "Europe/Amsterdam"
}

USER_RESPONSE: Final = {
    "email": "test@test.com",
    "display_name": "test",
    "language": "en",
    "country": "NL",
    "optIn": False,
    "optInApp": False,
}

SECURITY_RESPONSE: Final = {
    "enabled": True,
    "autolock": False
}

GENERIC_RESPONSE: Final = {
    "alm_sn": "test_sn",
    "service_counter": 69272,
    "needs_service": False,
    "alm_mode": "smart",
    "bareToolnumber": "3600HB0102",
    "alm_firmware_version": "17329.01211",
}

LAST_CUTTING_RESPONSE: Final = {
    "last_mowed": "2020-06-29T12:24:03.664+02:00"
}

NEXT_CUTTING_RESPONSE: Final = {
    "mow_next": "2020-07-03T10:00:00+02:00"
}

NETWORK_RESPONSE: Final = {
    "mcc": 204,
    "mnc": 16,
    "rssi": -83
}

CONFIG_RESPONSE: Final = {
    "region": 0,
    "language": 14,
    "border_cut": 0,
    "is_pin_set": True,
    "wire_id": 4,
    "bump_sensitivity": 0,
    "alarm_mode": False,
}

OPERATING_RESPONSE: Final = {
    "runtime": {
        "total": {"operate": 81106, "charge": 11834},
        "session": {"operate": 12, "charge": 12},
    },
    "battery": {
        "voltage": 8.6,
        "cycles": 1,
        "discharge": 0.0,
        "ambient_temp": 23,
        "battery_temp": 23,
        "percent": 86,
    },
    "garden": {
        "id": 34,
        "name": 1,
        "signal_id": 4,
        "size": 80,
        "inner_bounds": 238,
        "cuts": 61172,
        "runtime": 12,
        "charge": 11834,
        "bumps": 183,
        "stops": 10,
        "last_mow": 6,
        "map_cell_size": 120,
    },
    "hmiKeys": 213,
}

PREDICTIVE_CALENDAR_RESPONSE: Final = {
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
                        {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0},
                        {"En": True, "StHr": 20, "StMin": 0, "EnHr": 23, "EnMin": 59},
                    ],
                },
            ],
        }
    ],
}

PREDICTIVE_SCHEDULE_RESPONSE: Final = {
    "schedule_days": [
        {
            "day": 1,
            "slots": [{"En": True, "StHr": 10, "StMin": 0, "EnHr": 13, "EnMin": 0}],
        },
        {
            "day": 3,
            "slots": [{"En": True, "StHr": 11, "StMin": 0, "EnHr": 14, "EnMin": 0}],
        },
        {
            "day": 5,
            "slots": [{"En": True, "StHr": 10, "StMin": 0, "EnHr": 13, "EnMin": 0}],
        },
    ],
    "exclusion_days": [
        {
            "day": 0,
            "slots": [
                {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0, "Attr": "C"},
                {
                    "En": True,
                    "StHr": 20,
                    "StMin": 0,
                    "EnHr": 23,
                    "EnMin": 59,
                    "Attr": "C",
                },
            ],
        },
        {
            "day": 1,
            "slots": [
                {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0, "Attr": "C"},
                {
                    "En": True,
                    "StHr": 20,
                    "StMin": 0,
                    "EnHr": 23,
                    "EnMin": 59,
                    "Attr": "C",
                },
            ],
        },
        {
            "day": 2,
            "slots": [
                {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0, "Attr": "C"},
                {
                    "En": True,
                    "StHr": 8,
                    "StMin": 0,
                    "EnHr": 20,
                    "EnMin": 0,
                    "Attr": "P",
                },
                {
                    "En": True,
                    "StHr": 20,
                    "StMin": 0,
                    "EnHr": 23,
                    "EnMin": 59,
                    "Attr": "C",
                },
            ],
        },
        {
            "day": 3,
            "slots": [
                {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0, "Attr": "C"},
                {
                    "En": True,
                    "StHr": 8,
                    "StMin": 0,
                    "EnHr": 11,
                    "EnMin": 0,
                    "Attr": "p",
                },
                {
                    "En": True,
                    "StHr": 20,
                    "StMin": 0,
                    "EnHr": 23,
                    "EnMin": 59,
                    "Attr": "C",
                },
            ],
        },
        {
            "day": 4,
            "slots": [
                {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0, "Attr": "C"},
                {
                    "En": True,
                    "StHr": 8,
                    "StMin": 0,
                    "EnHr": 11,
                    "EnMin": 0,
                    "Attr": "Pp",
                },
                {
                    "En": True,
                    "StHr": 20,
                    "StMin": 0,
                    "EnHr": 23,
                    "EnMin": 59,
                    "Attr": "C",
                },
            ],
        },
        {
            "day": 5,
            "slots": [
                {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0, "Attr": "C"},
                {
                    "En": True,
                    "StHr": 20,
                    "StMin": 0,
                    "EnHr": 23,
                    "EnMin": 59,
                    "Attr": "C",
                },
            ],
        },
        {
            "day": 6,
            "slots": [
                {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0, "Attr": "C"},
                {"En": True, "StHr": 8, "StMin": 0, "EnHr": 9, "EnMin": 0, "Attr": "D"},
                {
                    "En": True,
                    "StHr": 20,
                    "StMin": 0,
                    "EnHr": 23,
                    "EnMin": 59,
                    "Attr": "C",
                },
            ],
        },
    ],
}

STATE_RESPONSE: Final = {
    "state": 64513,
    "map_update_available": True,
    "mowed": 97,
    "mowmode": 2,
    "xPos": 5,
    "yPos": 50,
    "runtime": {
        "total": {"operate": 81329, "charge": 11912},
        "session": {"operate": 10, "charge": 0},
    },
    "mapsvgcache_ts": 1593609416617,
    "svg_xPos": 720,
    "svg_yPos": 424,
    "config_change": False,
    "mow_trig": True,
}

STATE_UPDATE_RESPONSE: Final = {
    "state": 513,
}

STATE_FULL_UPDATE_RESPONSE: Final = {
    "state": 513,
    "map_update_available": True,
    "mowed": 97,
    "mowmode": 2,
    "xPos": 5,
    "yPos": 50,
    "runtime": {
        "total": {"operate": 81329, "charge": 11912},
        "session": {"operate": 10, "charge": 0},
    },
    "mapsvgcache_ts": 1593609416617,
    "svg_xPos": 720,
    "svg_yPos": 424,
    "config_change": False,
    "mow_trig": True,
}

test_config = {"serial": "123456789", "token": "testtoken"}


# endregion Test data


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class SyncMock(MagicMock):
    def __call__(self, *args, **kwargs):
        return super(SyncMock, self).__call__(*args, **kwargs)


class MockResponseAsync:
    """Class for mock responses in async."""

    def __init__(self, json, status):
        """Init the async mock response."""
        self._json = json
        self.status = status

    async def json(self):
        """Return json."""
        return self._json

    @property
    def content_type(self):
        """Return content type."""
        if self._json is not None:
            return CONTENT_TYPE_JSON
        return None

    async def __aexit__(self, exc_type, exc, tb):
        """Do async exit."""
        pass

    async def __aenter__(self):
        """Do async enter."""
        return self


class MockResponseSync:
    """Class for mock responses in sync."""

    def __init__(self, json, status):
        """Init the sync mock response."""
        self._json = json
        self.status_code = status

    def json(self):
        """Return json."""
        return self._json

    @property
    def headers(self):
        """Return header."""
        if self._json is not None:
            return {CONTENT_TYPE: f"{CONTENT_TYPE_JSON};"}
        return None


class TestIndego(object):
    """States class."""

    def test_repr(self):
        """Test the representation string."""
        indego = IndegoClient(**test_config)
        str(indego)

    @pytest.mark.parametrize(
        "state, json, checks",
        [
            (Alert, ALERT_RESPONSE, ["alm_sn"]),
            (OperatingData, OPERATING_RESPONSE, ["hmiKeys", ("garden.id", "['garden']['id']")]),
            (
                    Calendar,
                    CALENDAR_RESPONSE,
                    [
                        "cal",
                        ("days[0].day", "['days'][0]['day']"),
                        ("days[0].slots[0].En", "['days'][0]['slots'][0]['En']"),
                    ],
            ),
            (State, STATE_RESPONSE, ["state"]),
        ],
    )
    def test_states(self, state, json, checks):
        """Test States classes."""
        state_instance = state(**json)  # noqa: F841, pylint: disable=unused-variable
        for check in checks:
            if isinstance(check, str):
                value_state = eval(f"state_instance.{check}")
                value_json = eval(f"json['{check}']")
            else:
                value_state = eval(f"state_instance.{check[0]}")
                value_json = eval(f"json{check[1]}")
            assert value_state == value_json

    @pytest.mark.parametrize(
        "date_str, date_dt",
        [
            (
                    "2020-07-01T13:22:43.15+02:00",
                    datetime.fromisoformat("2020-07-01 13:22:43.150000+02:00"),
            ),
            (
                    "2020-07-03T10:00:00+02:00",
                    datetime.fromisoformat("2020-07-03 10:00:00+02:00"),
            ),
            (
                    datetime.fromisoformat("2020-07-03 10:00:00+02:00"),
                    datetime.fromisoformat("2020-07-03 10:00:00+02:00"),
            ),
            (None, None),
        ],
    )
    def test_date_parsing(self, date_str, date_dt):
        """Test the convert_bosch_datetime function."""
        test_dt = convert_bosch_datetime(date_str)
        assert test_dt == date_dt

    @pytest.mark.parametrize(
        "sync, func, attr, ret_value, assert_value",
        [
            (
                    True,
                    IndegoClient.update_calendar,
                    "calendar",
                    {"sel_cal": 3, "cals": [CALENDAR_RESPONSE]},
                    Calendar(**CALENDAR_RESPONSE),
            ),
            (
                    True,
                    IndegoClient.update_alerts,
                    "alerts",
                    [ALERT_RESPONSE],
                    [Alert(**ALERT_RESPONSE)]
            ),
            (
                    True,
                    IndegoClient.update_config,
                    "config",
                    CONFIG_RESPONSE,
                    Config(**CONFIG_RESPONSE)
            ),
            (
                    True,
                    IndegoClient.update_generic_data,
                    "generic_data",
                    GENERIC_RESPONSE,
                    GenericData(**GENERIC_RESPONSE),
            ),
            (
                    True,
                    IndegoClient.update_last_completed_mow,
                    "last_completed_mow",
                    {"last_mowed": "2020-07-01T13:22:43.15+02:00"},
                    datetime.fromisoformat("2020-07-01 13:22:43.150000+02:00"),
            ),
            (
                    True,
                    IndegoClient.update_location,
                    "location",
                    LOCATION_RESPONSE,
                    Location(**LOCATION_RESPONSE),
            ),
            (
                    True,
                    IndegoClient.update_network,
                    "network",
                    NETWORK_RESPONSE,
                    Network(**NETWORK_RESPONSE)
            ),
            (
                    True,
                    IndegoClient.update_next_mow,
                    "next_mow",
                    {"mow_next": "2020-07-03T10:00:00+02:00"},
                    datetime.fromisoformat("2020-07-03 10:00:00+02:00"),
            ),
            (
                    True,
                    IndegoClient.update_operating_data,
                    "operating_data",
                    OPERATING_RESPONSE,
                    OperatingData(**OPERATING_RESPONSE),
            ),
            (
                    True,
                    IndegoClient.update_predictive_calendar,
                    "predictive_calendar",
                    PREDICTIVE_CALENDAR_RESPONSE,
                    Calendar(**PREDICTIVE_CALENDAR_RESPONSE["cals"][0]),
            ),
            (
                    True,
                    IndegoClient.update_predictive_schedule,
                    "predictive_schedule",
                    PREDICTIVE_SCHEDULE_RESPONSE,
                    PredictiveSchedule(**PREDICTIVE_SCHEDULE_RESPONSE),
            ),
            (
                    True,
                    IndegoClient.update_security,
                    "security",
                    SECURITY_RESPONSE,
                    Security(**SECURITY_RESPONSE),
            ),
            (
                    True,
                    IndegoClient.update_setup,
                    "setup",
                    SETUP_RESPONSE,
                    Setup(**SETUP_RESPONSE)
            ),
            (
                    True,
                    IndegoClient.update_state,
                    "state",
                    STATE_RESPONSE,
                    State(**STATE_RESPONSE)
            ),
            (
                    True,
                    IndegoClient.update_updates_available,
                    "update_available",
                    {"available": False},
                    False,
            ),
            (
                    True,
                    IndegoClient.update_user,
                    "user",
                    USER_RESPONSE,
                    User(**USER_RESPONSE)
            ),
            (
                    True,
                    IndegoClient.update_all,
                    "user",
                    None,
                    None
            ),
            (
                    False,
                    IndegoAsyncClient.update_calendar,
                    "calendar",
                    {"sel_cal": 3, "cals": [CALENDAR_RESPONSE]},
                    Calendar(**CALENDAR_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_alerts,
                    "alerts",
                    [ALERT_RESPONSE],
                    [Alert(**ALERT_RESPONSE)],
            ),
            (
                    False,
                    IndegoAsyncClient.update_config,
                    "config",
                    CONFIG_RESPONSE,
                    Config(**CONFIG_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_generic_data,
                    "generic_data",
                    GENERIC_RESPONSE,
                    GenericData(**GENERIC_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_last_completed_mow,
                    "last_completed_mow",
                    {"last_mowed": "2020-07-01T13:22:43.15+02:00"},
                    datetime.fromisoformat("2020-07-01 13:22:43.150000+02:00"),
            ),
            (
                    False,
                    IndegoAsyncClient.update_location,
                    "location",
                    LOCATION_RESPONSE,
                    Location(**LOCATION_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_network,
                    "network",
                    NETWORK_RESPONSE,
                    Network(**NETWORK_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_next_mow,
                    "next_mow",
                    {"mow_next": "2020-07-03T10:00:00+02:00"},
                    datetime.fromisoformat("2020-07-03 10:00:00+02:00"),
            ),
            (
                    False,
                    IndegoAsyncClient.update_operating_data,
                    "operating_data",
                    OPERATING_RESPONSE,
                    OperatingData(**OPERATING_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_predictive_calendar,
                    "predictive_calendar",
                    PREDICTIVE_CALENDAR_RESPONSE,
                    Calendar(**PREDICTIVE_CALENDAR_RESPONSE["cals"][0]),
            ),
            (
                    False,
                    IndegoAsyncClient.update_predictive_schedule,
                    "predictive_schedule",
                    PREDICTIVE_SCHEDULE_RESPONSE,
                    PredictiveSchedule(**PREDICTIVE_SCHEDULE_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_security,
                    "security",
                    SECURITY_RESPONSE,
                    Security(**SECURITY_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_setup,
                    "setup",
                    SETUP_RESPONSE,
                    Setup(**SETUP_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_state,
                    "state",
                    STATE_RESPONSE,
                    State(**STATE_RESPONSE)
            ),
            (
                    False,
                    IndegoAsyncClient.update_updates_available,
                    "update_available",
                    {"available": False},
                    False,
            ),
            (
                    False,
                    IndegoAsyncClient.update_user,
                    "user",
                    USER_RESPONSE,
                    User(**USER_RESPONSE)
            ),
            (
                    False,
                    IndegoAsyncClient.update_all,
                    "user",
                    None,
                    None
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_client_update_functions(
            self, sync, func, attr, ret_value, assert_value
    ):
        """Test the base client functions with 200."""
        if sync:
            resp = MockResponseSync(ret_value, 200)
            with patch("requests.request", return_value=resp):
                indego = IndegoClient(**test_config)
                func(indego)
                assert getattr(indego, attr) == assert_value
                if attr == "state":
                    assert indego.state_description == "Docked"
                    assert indego.state_description_detail == "Sleeping"
        else:
            resp = MockResponseAsync(ret_value, 200)
            with patch("aiohttp.ClientSession.request", return_value=resp), patch(
                    "pyIndego.IndegoAsyncClient.start", return_value=True
            ):
                async with IndegoAsyncClient(**test_config) as indego:
                    await func(indego)
                    assert getattr(indego, attr) == assert_value
                    if attr == "state":
                        assert indego.state_description == "Docked"
                        assert indego.state_description_detail == "Sleeping"

    @pytest.mark.parametrize(
        "sync, func, param, attr, ret_value, assert_value",
        [
            (
                    True,
                    IndegoClient.update_state,
                    {"force": True},
                    "state",
                    STATE_RESPONSE,
                    State(**STATE_RESPONSE),
            ),
            (
                    True,
                    IndegoClient.update_state,
                    {"longpoll": True},
                    "state",
                    STATE_RESPONSE,
                    State(**STATE_RESPONSE),
            ),
            (
                    True,
                    IndegoClient.update_state,
                    {"force": True, "longpoll": True},
                    "state",
                    STATE_RESPONSE,
                    State(**STATE_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_state,
                    {"force": True},
                    "state",
                    STATE_RESPONSE,
                    State(**STATE_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_state,
                    {"longpoll": True},
                    "state",
                    STATE_RESPONSE,
                    State(**STATE_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_state,
                    {"force": True, "longpoll": True},
                    "state",
                    STATE_RESPONSE,
                    State(**STATE_RESPONSE),
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_client_update_state_params(
            self, sync, func, param, attr, ret_value, assert_value
    ):
        """Test the base client functions with 200."""
        if sync:
            resp = MockResponseSync(ret_value, 200)
            with patch("requests.request", return_value=resp):
                indego = IndegoClient(**test_config)
                func(indego, **param)
                assert getattr(indego, attr) == assert_value
        else:
            resp = MockResponseAsync(ret_value, 200)
            with patch("aiohttp.ClientSession.request", return_value=resp), patch(
                    "pyIndego.IndegoAsyncClient.start", return_value=True
            ):
                async with IndegoAsyncClient(**test_config) as indego:
                    await func(indego, **param)
                    assert getattr(indego, attr) == assert_value

    @pytest.mark.parametrize(
        "sync, func, initial_ret_value, updated_ret_value, initial_assert_value, updated_assert_value",
        [
            (
                    True,
                    IndegoClient.update_state,
                    STATE_RESPONSE,
                    None,  # No update / empty response
                    State(**STATE_RESPONSE),
                    State(**STATE_RESPONSE),
            ),
            (
                    True,
                    IndegoClient.update_state,
                    STATE_RESPONSE,
                    None,  # No update / empty response
                    State(**STATE_RESPONSE),
                    State(**STATE_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_state,
                    STATE_RESPONSE,
                    STATE_UPDATE_RESPONSE,
                    State(**STATE_RESPONSE),
                    State(**STATE_FULL_UPDATE_RESPONSE),
            ),
            (
                    False,
                    IndegoAsyncClient.update_state,
                    STATE_RESPONSE,
                    STATE_UPDATE_RESPONSE,
                    State(**STATE_RESPONSE),
                    State(**STATE_FULL_UPDATE_RESPONSE),
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_state_long_poll_updates(
            self, sync, func, initial_ret_value, updated_ret_value, initial_assert_value, updated_assert_value
    ):
        """Test a state update using longpoll and make sure the state of correctly merged."""
        if sync:
            indego = IndegoClient(**test_config)

            # Initial update with changes.
            resp = MockResponseSync(initial_ret_value, 200)
            with patch("requests.request", return_value=resp):
                func(indego, longpoll=True, longpoll_timeout=10)
                assert getattr(indego, "state") == initial_assert_value

            # 2nd update, state should be merged with previous update.
            resp = MockResponseSync(updated_ret_value, 504 if updated_ret_value is None else 200)
            with patch("requests.request", return_value=resp):
                func(indego, longpoll=True, longpoll_timeout=10)
                assert getattr(indego, "state") == updated_assert_value

        else:
            async with IndegoAsyncClient(**test_config) as indego:
                # Initial update with changes.
                resp = MockResponseAsync(initial_ret_value, 200)
                with patch("aiohttp.ClientSession.request", return_value=resp), patch(
                        "pyIndego.IndegoAsyncClient.start", return_value=True
                ):
                    await func(indego, longpoll=True, longpoll_timeout=10)
                    assert getattr(indego, "state") == initial_assert_value

                # 2nd update, state should be merged with previous update.
                resp = MockResponseAsync(updated_ret_value, 504 if updated_ret_value is None else 200)
                with patch("aiohttp.ClientSession.request", return_value=resp), patch(
                        "pyIndego.IndegoAsyncClient.start", return_value=True
                ):
                    await func(indego, longpoll=True, longpoll_timeout=10)
                    assert getattr(indego, "state") == updated_assert_value

    @pytest.mark.parametrize(
        "sync, func, attr, ret_value, assert_value",
        [
            (True, IndegoClient.update_user, "user", USER_RESPONSE, User(**USER_RESPONSE)),
            (False, IndegoAsyncClient.update_user, "user", USER_RESPONSE, User(**USER_RESPONSE)),
        ],
    )
    @pytest.mark.asyncio
    async def test_client_replace(self, sync, func, attr, ret_value, assert_value):
        """Test the base client functions with 200."""
        if sync:
            resp = MockResponseSync(ret_value, 200)
            with patch("requests.request", return_value=resp):
                indego = IndegoClient(**test_config)
                func(indego)
                assert getattr(indego, attr) == assert_value
                func(indego)
                assert getattr(indego, attr) == assert_value
        else:
            resp = MockResponseAsync(ret_value, 200)
            with patch("aiohttp.ClientSession.request", return_value=resp), patch(
                    "pyIndego.IndegoAsyncClient.start", return_value=True
            ):
                async with IndegoAsyncClient(**test_config) as indego:
                    await func(indego)
                    assert getattr(indego, attr) == assert_value
                    await func(indego)
                    assert getattr(indego, attr) == assert_value

    @pytest.mark.parametrize(
        "sync, response, func, attr, ret_value",
        [
            (True, 204, IndegoClient.update_user, "user", USER_RESPONSE),
            (True, 400, IndegoClient.update_user, "user", USER_RESPONSE),
            (True, 401, IndegoClient.update_user, "user", USER_RESPONSE),
            (True, 403, IndegoClient.update_user, "user", USER_RESPONSE),
            (True, 405, IndegoClient.update_user, "user", USER_RESPONSE),
            (True, 501, IndegoClient.update_user, "user", USER_RESPONSE),
            (True, 504, IndegoClient.update_user, "user", USER_RESPONSE),
            (False, 204, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
            (False, 400, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
            (False, 401, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
            (False, 403, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
            (False, 405, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
            (False, 501, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
            (False, 504, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
        ],
    )
    @pytest.mark.asyncio
    async def test_client_responses(self, sync, response, func, attr, ret_value):
        """Test the request functions with different responses."""
        if sync:
            resp = MockResponseSync(ret_value, response)
            with patch("requests.request", return_value=resp):
                indego = IndegoClient(**test_config)
                func(indego)
                assert getattr(indego, attr) == None
        else:
            resp = MockResponseAsync(ret_value, response)
            with patch("aiohttp.ClientSession.request", return_value=resp):
                async with IndegoAsyncClient(**test_config) as indego:
                    await func(indego)
                    assert getattr(indego, attr) == None

    @pytest.mark.parametrize(
        "error",
        [
            (asyncio.CancelledError),
            (Exception),
            (asyncio.TimeoutError),
            (ServerTimeoutError),
            (HTTPGatewayTimeout),
            (ClientOSError),
            (TooManyRedirects),
            (ClientResponseError),
            (SocketError),
        ],
    )
    @pytest.mark.asyncio
    async def test_a_client_response_errors(self, error):
        """Test the request functions with different responses."""
        with patch("aiohttp.ClientSession.request", side_effect=error), patch(
                "asyncio.sleep", new_callable=AsyncMock
        ):
            async with IndegoAsyncClient(**test_config) as indego:
                resp = await indego._request(
                    method=Methods.GET, path="alerts", timeout=1
                )
                assert resp is None

    @pytest.mark.parametrize(
        "error", [(Exception), (Timeout), (reqTooManyRedirects), (RequestException)]
    )
    def test_client_response_errors(self, error):
        """Test the request functions with different responses."""
        with patch("requests.request", side_effect=error), patch(
                "time.sleep", new_callable=SyncMock
        ):
            indego = IndegoClient(**test_config)
            resp = indego._request(method=Methods.GET, path="alerts", timeout=1)
            assert resp is None

    @pytest.mark.parametrize(  # noqa: ignore:C901
        "alerts, loaded, index, error",
        [
            ([Alert(**ALERT_RESPONSE)], True, 0, None),
            ([Alert(**ALERT_RESPONSE)], True, 1, IndexError),
            (None, True, 0, ValueError),
            (None, False, 0, ValueError),
        ],
    )
    @pytest.mark.asyncio
    async def test_alert_functions(self, alerts, loaded, index, error):
        """Test the function for handling alerts."""
        resp = MockResponseSync(True, 200)
        with patch("requests.request", return_value=resp):
            indego = IndegoClient(**test_config)
            indego.alerts = alerts
            indego._alerts_loaded = loaded
            try:
                res = indego.delete_alert(index)
                if error and not loaded:
                    assert False
                elif not alerts and loaded:
                    assert res is None
                else:
                    assert res
            except error:
                assert True
            try:
                res = indego.put_alert_read(index)
                if error and not loaded:
                    assert False
                elif not alerts and loaded:
                    assert res is None
                else:
                    assert res
            except error:
                assert True
            try:
                res = indego.delete_all_alerts()
                if alerts is None and loaded:
                    assert res is None
                else:
                    assert res
            except error:
                assert True
            try:
                res = indego.put_all_alerts_read()
                if alerts is None and loaded:
                    assert res is None
                else:
                    assert res
            except error:
                assert True
        resp = MockResponseAsync(True, 200)
        with patch("aiohttp.ClientSession.request", return_value=resp), patch(
                "pyIndego.IndegoAsyncClient.start", return_value=True
        ):
            async with IndegoAsyncClient(**test_config) as indego:
                indego.alerts = alerts
                indego._alerts_loaded = loaded
                try:
                    res = await indego.delete_alert(index)
                    if error and not loaded:
                        assert False
                    elif not alerts and loaded:
                        assert res is None
                    else:
                        assert res
                except error:
                    assert True
                try:
                    res = await indego.put_alert_read(index)
                    if error and not loaded:
                        assert False
                    elif not alerts and loaded:
                        assert res is None
                    else:
                        assert res
                except error:
                    assert True
                try:
                    res = await indego.delete_all_alerts()
                    if alerts is None and loaded:
                        assert res is None
                    else:
                        assert res
                except error:
                    assert True
                try:
                    res = await indego.put_all_alerts_read()
                    if alerts is None and loaded:
                        assert res is None
                    else:
                        assert res
                except error:
                    assert True

    @pytest.mark.parametrize(  # noqa: ignore:C901
        "command, param, error",
        [
            ("command", "mow", None),
            ("command", "pause", None),
            ("command", "returnToDock", None),
            ("command", "mows", ValueError),
            ("mow_mode", "true", None),
            ("mow_mode", "false", None),
            ("mow_mode", "True", None),
            ("mow_mode", "False", None),
            ("mow_mode", True, None),
            ("mow_mode", False, None),
            ("mow_mode", "mows", ValueError),
            ("pred_cal", None, None),
            ("pred_cal", {"cals": 1}, ValueError),
        ],
    )
    @pytest.mark.asyncio
    async def test_commands(self, command, param, error):
        """Test the function for handling alerts."""
        resp = MockResponseSync(True, 200)
        with patch("requests.request", return_value=resp):
            indego = IndegoClient(**test_config)
            if command == "command":
                try:
                    indego.put_command(param)
                    if error:
                        assert False
                    assert True
                except error:
                    assert True
            elif command == "mow_mode":
                try:
                    indego.put_mow_mode(param)
                    if error:
                        assert False
                    assert True
                except error:
                    assert True
            elif command == "pred_cal":
                try:
                    if param:
                        indego.put_predictive_cal(param)
                    else:
                        indego.put_predictive_cal()
                    if error:
                        assert False
                    assert True
                except error:
                    assert True

        resp = MockResponseAsync(True, 200)
        with patch("aiohttp.ClientSession.request", return_value=resp), patch(
                "pyIndego.IndegoAsyncClient.start", return_value=True
        ):
            async with IndegoAsyncClient(**test_config) as indego:
                if command == "command":
                    try:
                        await indego.put_command(param)
                        if error:
                            assert False
                        assert True
                    except error:
                        assert True
                elif command == "mow_mode":
                    try:
                        await indego.put_mow_mode(param)
                        if error:
                            assert False
                        assert True
                    except error:
                        assert True
                elif command == "pred_cal":
                    try:
                        if param:
                            await indego.put_predictive_cal(param)
                        else:
                            await indego.put_predictive_cal()
                        if error:
                            assert False
                        assert True
                    except error:
                        assert True

    @pytest.mark.parametrize(
        "config, param, error",
        [(None, None, ValueError), (None, "test.svg", None), ("test.svg", None, None)],
    )
    @pytest.mark.asyncio
    async def test_download(self, config, param, error):
        """Test the function for download map."""
        conf = test_config.copy()
        if config:
            conf.update({"map_filename": config})
        with patch("pyIndego.IndegoClient.get", return_value=None):
            indego = IndegoClient(**conf)
            try:
                indego.download_map(param)
                assert indego.map_filename == "test.svg"
                if error:
                    assert False
            except error:
                assert True

        with patch("pyIndego.IndegoAsyncClient.start", return_value=True), patch(
                "pyIndego.IndegoAsyncClient.get", return_value=None
        ):
            async with IndegoAsyncClient(**conf) as indego:
                try:
                    await indego.download_map(param)
                    assert indego.map_filename == "test.svg"
                    if error:
                        assert False
                except error:
                    assert True

    def test_update_battery(self):
        """Test the battery update function."""
        indego = IndegoClient(**test_config)
        indego._update_generic_data(GENERIC_RESPONSE)
        indego._update_operating_data(OPERATING_RESPONSE)

