import aiohttp
import asyncio
import inspect
import logging
import json

from pyIndego import IndegoAsyncClient
from pyIndego.const import DEFAULT_BODY, Methods

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


async def main(config):
    async with IndegoAsyncClient(**config) as indego:
        await indego.update_state(longpoll=True)
        print(indego.state)
        # await indego.update_next_mow()
        # await indego.update_generic_data()
        # print(indego.generic_data)
        # print(indego.calendar)
        # print(indego.calendar.days[1])
        # print(indego.next_mow)
        # print(update_list)
        # await indego.update_all()
        # await indego.update_state()
        # print(indego.state)
        # await indego.update_alerts()
        # print("Alerts ", indego.alerts)
        # print("State ", indego.state)
        # strings = [
        #     "alms/903600532/predictive/lastcutting",
        #     "alms/903600532/predictive/useradjustment",
        #     "alms/903600532/predictive/weather",
        #     "alms/903600532/calendar",
        #     "alms/903600532/predictive/calendar",
        # ]
        # for s in strings:
        #     print(await indego._request(Methods.GET, s))
        # await indego.put_alert_read(0, True)
        # await indego.delete_alert(0)

        # await indego.update_alerts()
        # print("After ", indego.alerts)


if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    # config.pop("serial")
    # config["username"] = "sdjbfajhbsdf"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(config))
