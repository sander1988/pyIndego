"""Test the states of pyIndego."""
from datetime import datetime
import pytest
from mock import patch
import logging
from aiohttp import web
import json

from pyIndego import IndegoAsyncClient, IndegoClient
from pyIndego.const import CONTENT_TYPE_JSON, CONTENT_TYPE
from pyIndego.helpers import convert_bosch_datetime
from pyIndego.states import (
    Alert,
    Battery,
    CalendarSlot,
    CalendarDay,
    Calendar,
    GenericData,
    Location,
    Network,
    Config,
    Setup,
    Security,
    RuntimeDetail,
    Runtime,
    Garden,
    OperatingData,
    State,
    User,
)

_LOGGER = logging.getLogger(__name__)

alert = {
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
calendar = {
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
setup_json = {
    "hasOwner": True,
    "hasPin": True,
    "hasMap": True,
    "hasAutoCal": False,
    "hasIntegrityCheckPassed": True,
}
location = {"latitude": "1.1234", "longitude": "1.1234", "timezone": "Europe/Amsterdam"}
user = {
    "email": "test@test.com",
    "display_name": "test",
    "language": "en",
    "country": "NL",
    "optIn": False,
    "optInApp": False,
}
security = {"enabled": True, "autolock": False}
generic = {
    "alm_sn": "test_sn",
    "service_counter": 69272,
    "needs_service": False,
    "alm_mode": "smart",
    "bareToolnumber": "3600HB0102",
    "alm_firmware_version": "17329.01211",
}
lastcutting = {"last_mowed": "2020-06-29T12:24:03.664+02:00"}
nextcutting = {"mow_next": "2020-07-03T10:00:00+02:00"}
network = {"mcc": 204, "mnc": 16, "rssi": -83}
config = {
    "region": 0,
    "language": 14,
    "border_cut": 0,
    "is_pin_set": True,
    "wire_id": 4,
    "bump_sensitivity": 0,
    "alarm_mode": False,
}
operating = {
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
state = {
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

test_config = {"username": "testname", "password": "testpassword", "api_url": ""}


class MockResponseAsync:
    def __init__(self, json, status):
        self._json = json
        self.status = status

    async def json(self):
        return self._json

    @property
    def content_type(self):
        return CONTENT_TYPE_JSON

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


class MockResponseSync:
    def __init__(self, json, status):
        self._json = json
        self.status_code = status

    def json(self):
        return self._json

    @property
    def headers(self):
        return {CONTENT_TYPE: f"{CONTENT_TYPE_JSON};"}


class TestIndego(object):
    """States class."""

    @pytest.mark.parametrize(
        "state, json, checks",
        [
            (Alert, alert, ["alm_sn"]),
            (OperatingData, operating, ["hmiKeys", ("garden.id", "['garden']['id']")]),
            (
                Calendar,
                calendar,
                [
                    "cal",
                    ("days[0].day", "['days'][0]['day']"),
                    ("days[0].slots[0].En", "['days'][0]['slots'][0]['En']"),
                ],
            ),
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
        ],
    )
    def test_date_parsing(self, date_str, date_dt):
        """Test the convert_bosch_datetime function."""
        test_dt = convert_bosch_datetime(date_str)
        assert test_dt == date_dt

    @pytest.mark.parametrize(
        "func, attr, ret_value, assert_value",
        [
            (
                IndegoAsyncClient.update_calendar,
                "calendar",
                {"sel_cal": 3, "cals": [calendar]},
                Calendar(**calendar),
            ),
            (IndegoAsyncClient.update_alerts, "alerts", [alert], [Alert(**alert)]),
            (IndegoAsyncClient.update_config, "config", config, Config(**config)),
            (
                IndegoAsyncClient.update_generic_data,
                "generic_data",
                generic,
                GenericData(**generic),
            ),
            (
                IndegoAsyncClient.update_last_completed_mow,
                "last_completed_mow",
                {"last_mowed": "2020-07-01T13:22:43.15+02:00"},
                datetime.fromisoformat("2020-07-01 13:22:43.150000+02:00"),
            ),
            (
                IndegoAsyncClient.update_location,
                "location",
                location,
                Location(**location),
            ),
            (IndegoAsyncClient.update_network, "network", network, Network(**network)),
            (
                IndegoAsyncClient.update_next_mow,
                "next_mow",
                {"mow_next": "2020-07-03T10:00:00+02:00"},
                datetime.fromisoformat("2020-07-03 10:00:00+02:00"),
            ),
            (
                IndegoAsyncClient.update_operating_data,
                "operating_data",
                operating,
                OperatingData(**operating),
            ),
            (
                IndegoAsyncClient.update_security,
                "security",
                security,
                Security(**security),
            ),
            (IndegoAsyncClient.update_setup, "setup", setup_json, Setup(**setup_json)),
            (IndegoAsyncClient.update_state, "state", state, State(**state)),
            (
                IndegoAsyncClient.update_updates_available,
                "update_available",
                {"available": False},
                False,
            ),
            (IndegoAsyncClient.update_user, "user", user, User(**user)),
        ],
    )
    async def test_client_update_functions(self, func, attr, ret_value, assert_value):
        """Test the base client functions with 200."""
        resp = MockResponseAsync(ret_value, 200)
        with patch("aiohttp.ClientSession.request", return_value=resp), patch(
            "pyIndego.IndegoAsyncClient.start", return_value=True
        ):
            async with IndegoAsyncClient(**test_config) as indegoA:
                indegoA._contextid = "askdjfbaks"
                indegoA._online = True
                indegoA._userid = "test_user_id"
                await func(indegoA)
                assert getattr(indegoA, attr) == assert_value

    @pytest.mark.parametrize(
        "response, func, attr, ret_value, assert_value",
        [
            (204, IndegoAsyncClient.update_user, "user", user, None),
            (400, IndegoAsyncClient.update_user, "user", user, None),
            (401, IndegoAsyncClient.update_user, "user", user, None),
            (403, IndegoAsyncClient.update_user, "user", user, None),
            (405, IndegoAsyncClient.update_user, "user", user, None),
            (501, IndegoAsyncClient.update_user, "user", user, None),
            (504, IndegoAsyncClient.update_user, "user", user, None),
        ],
    )
    async def test_client_responses(
        self, response, func, attr, ret_value, assert_value
    ):
        """Test the base client functions with different responses."""
        resp = MockResponseAsync(ret_value, response)
        with patch("aiohttp.ClientSession.request", return_value=resp):
            async with IndegoAsyncClient(**test_config) as indegoA:
                indegoA._online = True
                indegoA._userid = "test_user_id"
                await func(indegoA)
                assert getattr(indegoA, attr) == assert_value

    @pytest.mark.parametrize(
        "func, attr, ret_value, assert_value",
        [
            (
                IndegoClient.update_calendar,
                "calendar",
                {"sel_cal": 3, "cals": [calendar]},
                Calendar(**calendar),
            ),
            (IndegoClient.update_alerts, "alerts", [alert], [Alert(**alert)]),
            (IndegoClient.update_config, "config", config, Config(**config)),
            (
                IndegoClient.update_generic_data,
                "generic_data",
                generic,
                GenericData(**generic),
            ),
            (
                IndegoClient.update_last_completed_mow,
                "last_completed_mow",
                {"last_mowed": "2020-07-01T13:22:43.15+02:00"},
                datetime.fromisoformat("2020-07-01 13:22:43.150000+02:00"),
            ),
            (IndegoClient.update_location, "location", location, Location(**location)),
            (IndegoClient.update_network, "network", network, Network(**network)),
            (
                IndegoClient.update_next_mow,
                "next_mow",
                {"mow_next": "2020-07-03T10:00:00+02:00"},
                datetime.fromisoformat("2020-07-03 10:00:00+02:00"),
            ),
            (
                IndegoClient.update_operating_data,
                "operating_data",
                operating,
                OperatingData(**operating),
            ),
            (IndegoClient.update_security, "security", security, Security(**security)),
            (IndegoClient.update_setup, "setup", setup_json, Setup(**setup_json)),
            (IndegoClient.update_state, "state", state, State(**state)),
            (
                IndegoClient.update_updates_available,
                "update_available",
                {"available": False},
                False,
            ),
            (IndegoClient.update_user, "user", user, User(**user)),
        ],
    )
    def test_client_update_functions_sync(self, func, attr, ret_value, assert_value):
        """Test the base client functions with 200."""
        resp = MockResponseSync(ret_value, 200)
        with patch("requests.request", return_value=resp):
            indegoA = IndegoClient(**test_config)
            indegoA._online = True
            indegoA._userid = "test_user_id"
            func(indegoA)
            assert getattr(indegoA, attr) == assert_value

    @pytest.mark.parametrize(
        "response, func, attr, ret_value, assert_value",
        [
            (204, IndegoClient.update_user, "user", user, None),
            (400, IndegoClient.update_user, "user", user, None),
            (401, IndegoClient.update_user, "user", user, None),
            (403, IndegoClient.update_user, "user", user, None),
            (405, IndegoClient.update_user, "user", user, None),
            (501, IndegoClient.update_user, "user", user, None),
            (504, IndegoClient.update_user, "user", user, None),
        ],
    )
    def test_client_responses_sync(self, response, func, attr, ret_value, assert_value):
        """Test the base client functions with different responses."""
        resp = MockResponseSync(ret_value, response)
        with patch("requests.request", return_value=resp):
            indegoA = IndegoClient(**test_config)
            indegoA._online = True
            indegoA._userid = "test_user_id"
            func(indegoA)
            assert getattr(indegoA, attr) == assert_value
