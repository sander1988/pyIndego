import aiohttp
import asyncio
import logging
import json

from pyIndego import IndegoAsyncClient

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


async def main(config):
    async with IndegoAsyncClient(**config) as indego:
        await indego.update_all()
        # await asyncio.gather(
        #     *[
        #         # indego.update_generic_data(),
        #         indego.update_state(),
        #         # indego.update_last_completed_mow(),
        #         # indego.update_location(),
        #         # indego.update_next_mow(),
        #         indego.update_operating_data(),
        #         # indego.update_updates(),
        #         # indego.update_users(),
        #         # indego.update_network(),
        #         # indego.update_map()
        #         # indego.update_longpoll_state(120),
        #         # indego.update_alerts(),
        #     ]
        # )
        # print(indego)
        # print("map: ", indego.map_filename)
        # print("network ", indego.network)
        print("state: ", indego.state)
        print("state: ", indego.state.state)
        print("state description: ", indego.state_description)
        print("state descrption detail: ", indego.state_description_detail)
        # print("users: ", indego.users)
        # print("Generic data: ", indego.generic_data)
        # # print("Generic data min voltage: ", indego.generic_data.model_voltage.min)
        # # print("Alerts: ", indego.alerts)
        # print("Operating_data: ", indego.operating_data)
        # print("Battery: ", indego.operating_data.battery)
        # await indego.update_generic_data()
        # print("Generic data: ", indego.generic_data)
        # print("Battery: ", indego.operating_data.battery)
        # print("Session charge: ", indego.operating_data.runtime.session.charge)

        print("Next mow: ", indego.next_mow)
        # print("location: ", indego.location)
        print("last mow: ", indego.last_completed_mow)
        # print(indego.generic_data.alm_mode)
        # print(indego.alm_name)
        # print(indego.service_counter)
        # print(indego.needs_service)
        # print(indego.alm_mode)
        # print(indego.bare_tool_number)
        # print(indego.alm_firmware_version)
        # print(indego.model_description)
        # print(indego.model_voltage)
        # print(indego.mowing_mode_description)
        # print(indego.model_description)
        # print(indego.model_description)
        # print(indego.mower_state)
        # print(indego.mower_state_description)
        # print(indego.mower_state_description_detailed)
        # print(indego.battery)
        # print(indego.alerts_count)
        # print(indego.email)
        # print(indego.garden)
        # print(indego.x_pos, ", ", indego.y_pos)
        # indego.show_vars()


if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(config))
