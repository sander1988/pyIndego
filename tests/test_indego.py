"""Test the states of pyIndego."""
import asyncio
import logging
from datetime import datetime
from socket import error as SocketError

import pytest
from aiohttp import (
    ClientOSError,
    ClientResponseError,
    ServerTimeoutError,
    TooManyRedirects,
    web,
)
from aiohttp.web_exceptions import HTTPGatewayTimeout
from mock import MagicMock, patch
from requests.exceptions import HTTPError, RequestException, Timeout
from requests.exceptions import TooManyRedirects as reqTooManyRedirects

from pyIndego import IndegoAsyncClient, IndegoClient
from pyIndego.const import CONTENT_TYPE, CONTENT_TYPE_JSON, Methods
from pyIndego.helpers import convert_bosch_datetime
from pyIndego.states import (
    Alert,
    Battery,
    Calendar,
    CalendarDay,
    CalendarSlot,
    Config,
    Garden,
    GenericData,
    Location,
    Network,
    OperatingData,
    PredictiveSchedule,
    Runtime,
    RuntimeDetail,
    Security,
    Setup,
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
predictive_calendar = {
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

predictive_schedule = {
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

test_config = {"username": "testname", "password": "testpassword", "api_url": "", "serial": "123456789"}


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
        return CONTENT_TYPE_JSON

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
        return {CONTENT_TYPE: f"{CONTENT_TYPE_JSON};"}


class TestIndego(object):
    """States class."""

    def test_repr(self):
        """Test the representation string."""
        indego = IndegoClient(**test_config)
        str(indego)

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
            (State, state, ["state"]),
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
                {"sel_cal": 3, "cals": [calendar]},
                Calendar(**calendar),
            ),
            (True, IndegoClient.update_alerts, "alerts", [alert], [Alert(**alert)]),
            (True, IndegoClient.update_config, "config", config, Config(**config)),
            (
                True,
                IndegoClient.update_generic_data,
                "generic_data",
                generic,
                GenericData(**generic),
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
                location,
                Location(**location),
            ),
            (True, IndegoClient.update_network, "network", network, Network(**network)),
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
                operating,
                OperatingData(**operating),
            ),
            (
                True,
                IndegoClient.update_predictive_calendar,
                "predictive_calendar",
                predictive_calendar,
                Calendar(**predictive_calendar["cals"][0]),
            ),
            (
                True,
                IndegoClient.update_predictive_schedule,
                "predictive_schedule",
                predictive_schedule,
                PredictiveSchedule(**predictive_schedule),
            ),
            (
                True,
                IndegoClient.update_security,
                "security",
                security,
                Security(**security),
            ),
            (True, IndegoClient.update_setup, "setup", setup_json, Setup(**setup_json)),
            (True, IndegoClient.update_state, "state", state, State(**state)),
            (
                True,
                IndegoClient.update_updates_available,
                "update_available",
                {"available": False},
                False,
            ),
            (True, IndegoClient.update_user, "user", user, User(**user)),
            (True, IndegoClient.update_all, "user", None, None),
            (
                False,
                IndegoAsyncClient.update_calendar,
                "calendar",
                {"sel_cal": 3, "cals": [calendar]},
                Calendar(**calendar),
            ),
            (
                False,
                IndegoAsyncClient.update_alerts,
                "alerts",
                [alert],
                [Alert(**alert)],
            ),
            (
                False,
                IndegoAsyncClient.update_config,
                "config",
                config,
                Config(**config),
            ),
            (
                False,
                IndegoAsyncClient.update_generic_data,
                "generic_data",
                generic,
                GenericData(**generic),
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
                location,
                Location(**location),
            ),
            (
                False,
                IndegoAsyncClient.update_network,
                "network",
                network,
                Network(**network),
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
                operating,
                OperatingData(**operating),
            ),
            (
                False,
                IndegoAsyncClient.update_predictive_calendar,
                "predictive_calendar",
                predictive_calendar,
                Calendar(**predictive_calendar["cals"][0]),
            ),
            (
                False,
                IndegoAsyncClient.update_predictive_schedule,
                "predictive_schedule",
                predictive_schedule,
                PredictiveSchedule(**predictive_schedule),
            ),
            (
                False,
                IndegoAsyncClient.update_security,
                "security",
                security,
                Security(**security),
            ),
            (
                False,
                IndegoAsyncClient.update_setup,
                "setup",
                setup_json,
                Setup(**setup_json),
            ),
            (False, IndegoAsyncClient.update_state, "state", state, State(**state)),
            (
                False,
                IndegoAsyncClient.update_updates_available,
                "update_available",
                {"available": False},
                False,
            ),
            (False, IndegoAsyncClient.update_user, "user", user, User(**user)),
            (False, IndegoAsyncClient.update_all, "user", None, None),
        ],
    )
    async def test_client_update_functions(
        self, sync, func, attr, ret_value, assert_value
    ):
        """Test the base client functions with 200."""
        if sync:
            resp = MockResponseSync(ret_value, 200)
            with patch("requests.request", return_value=resp):
                indego = IndegoClient(**test_config)
                indego._online = True
                indego._userid = "test_user_id"
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
                    indego._contextid = "askdjfbaks"
                    indego._online = True
                    indego._userid = "test_user_id"
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
                state,
                State(**state),
            ),
            (
                True,
                IndegoClient.update_state,
                {"longpoll": True},
                "state",
                state,
                State(**state),
            ),
            (
                True,
                IndegoClient.update_state,
                {"force": True, "longpoll": True},
                "state",
                state,
                State(**state),
            ),
            (
                False,
                IndegoAsyncClient.update_state,
                {"force": True},
                "state",
                state,
                State(**state),
            ),
            (
                False,
                IndegoAsyncClient.update_state,
                {"longpoll": True},
                "state",
                state,
                State(**state),
            ),
            (
                False,
                IndegoAsyncClient.update_state,
                {"force": True, "longpoll": True},
                "state",
                state,
                State(**state),
            ),
        ],
    )
    async def test_client_update_state_params(
        self, sync, func, param, attr, ret_value, assert_value
    ):
        """Test the base client functions with 200."""
        if sync:
            resp = MockResponseSync(ret_value, 200)
            with patch("requests.request", return_value=resp):
                indego = IndegoClient(**test_config)
                indego._online = True
                indego._userid = "test_user_id"
                func(indego, **param)
                assert getattr(indego, attr) == assert_value
        else:
            resp = MockResponseAsync(ret_value, 200)
            with patch("aiohttp.ClientSession.request", return_value=resp), patch(
                "pyIndego.IndegoAsyncClient.start", return_value=True
            ):
                async with IndegoAsyncClient(**test_config) as indego:
                    indego._contextid = "askdjfbaks"
                    indego._online = True
                    indego._userid = "test_user_id"
                    await func(indego, **param)
                    assert getattr(indego, attr) == assert_value

    @pytest.mark.parametrize(
        "sync, func, attr, ret_value, assert_value",
        [
            (True, IndegoClient.update_user, "user", user, User(**user)),
            (False, IndegoAsyncClient.update_user, "user", user, User(**user)),
        ],
    )
    async def test_client_replace(self, sync, func, attr, ret_value, assert_value):
        """Test the base client functions with 200."""
        if sync:
            resp = MockResponseSync(ret_value, 200)
            with patch("requests.request", return_value=resp):
                indego = IndegoClient(**test_config)
                indego._online = True
                indego._userid = "test_user_id"
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
                    indego._contextid = "askdjfbaks"
                    indego._online = True
                    indego._userid = "test_user_id"
                    await func(indego)
                    assert getattr(indego, attr) == assert_value
                    await func(indego)
                    assert getattr(indego, attr) == assert_value

    @pytest.mark.parametrize(
        "sync, response, func, attr, ret_value",
        [
            (True, 204, IndegoClient.update_user, "user", user),
            (True, 400, IndegoClient.update_user, "user", user),
            (True, 401, IndegoClient.update_user, "user", user),
            (True, 403, IndegoClient.update_user, "user", user),
            (True, 405, IndegoClient.update_user, "user", user),
            (True, 501, IndegoClient.update_user, "user", user),
            (True, 504, IndegoClient.update_user, "user", user),
            (False, 204, IndegoAsyncClient.update_user, "user", user),
            (False, 400, IndegoAsyncClient.update_user, "user", user),
            (False, 401, IndegoAsyncClient.update_user, "user", user),
            (False, 403, IndegoAsyncClient.update_user, "user", user),
            (False, 405, IndegoAsyncClient.update_user, "user", user),
            (False, 501, IndegoAsyncClient.update_user, "user", user),
            (False, 504, IndegoAsyncClient.update_user, "user", user),
        ],
    )
    async def test_client_responses(self, sync, response, func, attr, ret_value):
        """Test the request functions with different responses."""
        if sync:
            resp = MockResponseSync(ret_value, response)
            with patch("requests.request", return_value=resp):
                indego = IndegoClient(**test_config)
                indego._online = True
                indego._userid = "test_user_id"
                func(indego)
                assert getattr(indego, attr) == None
        else:
            resp = MockResponseAsync(ret_value, response)
            with patch("aiohttp.ClientSession.request", return_value=resp):
                async with IndegoAsyncClient(**test_config) as indego:
                    indego._online = True
                    indego._userid = "test_user_id"
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
    async def test_a_client_response_errors(self, error):
        """Test the request functions with different responses."""
        with patch("aiohttp.ClientSession.request", side_effect=error), patch(
            "asyncio.sleep", new_callable=AsyncMock
        ):
            async with IndegoAsyncClient(**test_config) as indego:
                indego._online = True
                indego._userid = "test_user_id"
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
            indego._online = True
            indego._userid = "test_user_id"
            resp = indego._request(method=Methods.GET, path="alerts", timeout=1)
            assert resp is None

    @pytest.mark.parametrize(  # noqa: ignore:C901
        "alerts, loaded, index, error",
        [
            ([Alert(**alert)], True, 0, None),
            ([Alert(**alert)], True, 1, IndexError),
            (None, True, 0, ValueError),
            (None, False, 0, ValueError),
        ],
    )
    async def test_alert_functions(self, alerts, loaded, index, error):
        """Test the function for handling alerts."""
        resp = MockResponseSync(True, 200)
        with patch("requests.request", return_value=resp):
            indego = IndegoClient(**test_config)
            indego._online = True
            indego._userid = "test_user_id"
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
                indego._online = True
                indego._userid = "test_user_id"
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
    async def test_commands(self, command, param, error):
        """Test the function for handling alerts."""
        resp = MockResponseSync(True, 200)
        with patch("requests.request", return_value=resp):
            indego = IndegoClient(**test_config)
            indego._online = True
            indego._userid = "test_user_id"
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
                indego._online = True
                indego._userid = "test_user_id"
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
        "config",
        [
            ({"username": "testname", "password": "testpassword", "api_url": ""}),
            (
                {
                    "username": "testname",
                    "password": "testpassword",
                    "serial": "123456789",
                    "api_url": "",
                }
            ),
        ],
    )
    async def test_login(self, config):
        """Test the function for handling alerts."""
        resp_json = {"contextId": "98765", "userId": "12345"}
        resp_get = [{"alm_sn": "123456789"}]
        resp_login_s = MockResponseSync(resp_json, 200)
        with patch("requests.request", return_value=resp_login_s), patch(
            "pyIndego.IndegoClient.get", return_value=resp_get
        ):
            indego = IndegoClient(**config)
            indego.login()
            assert indego._userid == "12345"
            assert indego.serial == "123456789"

        resp_login_a = MockResponseAsync(resp_json, 200)
        with patch("aiohttp.ClientSession.request", return_value=resp_login_a), patch(
            "pyIndego.IndegoAsyncClient.start", return_value=True
        ), patch("pyIndego.IndegoAsyncClient.get", return_value=resp_get):
            async with IndegoAsyncClient(**config) as indego:
                await indego.login()
                assert indego._userid == "12345"
                assert indego.serial == "123456789"

    @pytest.mark.parametrize(
        "config, param, error",
        [(None, None, ValueError), (None, "test.svg", None), ("test.svg", None, None)],
    )
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
        indego._update_generic_data(generic)
        indego._update_operating_data(operating)
