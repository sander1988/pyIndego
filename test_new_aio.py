"""test aio client."""
import asyncio
import inspect
import json
import logging

import aiohttp

from pyIndego import IndegoAsyncClient
from pyIndego.const import Methods

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


async def main(config):
    """Test class of test aio."""
    async with IndegoAsyncClient(**config) as indego:
        # await indego.update_alerts()
        # print("alerts: ", indego.alerts)
        # print("alert count: ", indego.alerts_count)

        # await indego.update_calendar()
        # print("calendar: ", indego.calendar)
        # print("next mow: ", indego.next_mows)

        # await indego.update_config()
        # print("config: ", indego.config)

        # await indego.update_generic_data()
        # print("generic data: ", indego.generic_data)

        # await indego.update_last_completed_mow()
        # print("last completed mow: ", indego.last_completed_mow)

        # await indego.update_location()
        # print("location: ", indego.location)
        # print("next mows with tz: ", indego.next_mows_with_tz)

        # await indego.update_network()
        # print("network: ", indego.network)

        # await indego.update_next_mow()
        # print("next mow: ", indego.next_mow)

        # await indego.update_operating_data()
        # print("operating data: ", indego.operating_data)

        await indego.update_predictive_calendar()
        print("predictive calendar: ", indego.predictive_calendar)

        await indego.update_predictive_schedule()
        print("predictive schedule: ", indego.predictive_schedule)

        # await indego.update_security()
        # print("security: ", indego.security)

        # await indego.update_setup()
        # print("setup: ", indego.setup)

        # await indego.update_state()
        # print("state: ", indego.state)
        # print("state description: ", indego.state_description)
        # print("state description detail: ", indego.state_description_detail)

        # await indego.update_updates_available()
        # print("update available: ", indego.update_available)

        # await indego.update_user()
        # print("user: ", indego.user)

        # while True:
        #     await indego.update_state(longpoll=True, longpoll_timeout=300)
        #     print("state: ", indego.state)
        #     print("state description: ", indego.state_description)
        #     print("state description detail: ", indego.state_description_detail)


if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    # config.pop("serial")
    # config["username"] = "sdjbfajhbsdf"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(config))
