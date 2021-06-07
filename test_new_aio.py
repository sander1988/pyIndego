"""test aio client."""
import asyncio
import inspect
import json
import logging
import time
import datetime

import aiohttp

from pyIndego import IndegoAsyncClient
from pyIndego.const import Methods

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


async def main(config):
    """Test class of test aio."""
    async with IndegoAsyncClient(**config) as indego:
        #Update and cache all calls from API
        #await indego.update_all()
        
        # await indego.update_alerts()
        # print("alerts: ", indego.alerts)
        ###### FUNCTION! print("alert count: ", indego.alerts_count)

        # await indego.update_calendar()
        # print("calendar: ", indego.calendar)
        ###### FUNCTION! print("next mow: ", indego.next_mows)

        # await indego.update_config()
        # print("config: ", indego.config)

        # await indego.update_generic_data()
        # print("generic data: ", indego.generic_data)

        # await indego.update_last_completed_mow()
        # print("last completed mow: ", indego.last_completed_mow)

        # await indego.update_location()
        # print("location: ", indego.location)

        # await indego.update_network()
        # print("network: ", indego.network)

        # await indego.update_next_mow()
        # print("next mow: ", indego.next_mow)

        # await indego.update_operating_data()
        # print("operating data: ", indego.operating_data)

        # await indego.update_predictive_calendar()
        # print("predictive calendar: ", indego.predictive_calendar)
# 
        # await indego.update_predictive_schedule()
        # print("predictive schedule: ", indego.predictive_schedule)

        # await indego.update_security()
        # print("security: ", indego.security)

        # await indego.update_setup()
        # print("setup: ", indego.setup)
        jens = False
        while not (jens == True):
            await indego.update_state()
            #await indego.update_state(force=True)
            # print("state: ", indego.state)
            # print("state description: ", indego.state_description)
            # print("state description detail: ", indego.state_description_detail)
            # print("serial: ", indego.serial)
            #print("xPos: ", indego.state.xPos)
            #print("yPos: ", indego.state.yPos)
            
            f = open('percentage.log', 'a')
            
            from time import gmtime, strftime
            logtime = strftime("%H:%M", gmtime())
            print(logtime , end = ' ')
            print("Mowed: ", indego.state.mowed)
            

            
            
            
            f.write(str(logtime) + " - ")
            f.write(str(indego.state.mowed) + "\n")
            f.close()
            time.sleep(60)   # Delays for 5 seconds. You can also use a float value.

        # await indego.update_state(force=True)
        # print("state: ", indego.state)
        # print("Force xPos: ", indego.state.xPos)
        # print("Force yPos: ", indego.state.yPos)

        # Must call regular get_Sate before longpoll
        # await indego.update_state()
        # print("state: ", indego.state)
        # await indego.update_state(longpoll=True, longpoll_timeout=10)
        # print("state: ", indego.state)
        # print("state description: ", indego.state_description)
        # print("state description detail: ", indego.state_description_detail)

        
        # await indego.update_updates_available()
        # print("update available: ", indego.update_available)

        # await indego.update_user()
        # print("user: ", indego.user)



if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    # config.pop("serial")
    # config["username"] = "sdjbfajhbsdf"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(config))
