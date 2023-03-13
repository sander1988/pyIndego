import json
import logging
import pytz
import pytz    # $ pip install pytz
import tzlocal # $ pip install tzlocal
from pyIndego import IndegoClient
from datetime import datetime
import time

logging.basicConfig(filename="pyIndego.log", level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


def main(config):
    with IndegoClient(**config) as indego:
        # print(" ")
        # print("=[indego.download_map]===")
        # indego.download_map()
        # print("map: ", indego.map_filename)

        # print(" ")
        # print("=[indego.update_state]===")
        # indego.update_state()
        # print(indego.state)
        # print(f"State: {indego.state_description}")
        # print(f"State detail: {indego.state_description_detail}")
        #
        # print(f"xPos: {indego.state.xPos}")
        # print(f"yPos: {indego.state.yPos}")

        print(f"Mowers: {indego.get_mowers()}")

        print(f"Serial: {indego.serial}")
        #print(" ")
        #print("=[update_state longpoll]===")
        #indego.update_state(longpoll=True, longpoll_timeout=20)
        #print(indego.state)
        #print(indego.state_description)
        #print(indego.state_description_detail)

        #print(" ")
        #print("=[indego.update_alerts]====")
        #indego.update_alerts()
        #print(indego.alerts)
        #print("=[indego.alerts_count]====")
        #print(indego.alerts_count)
        #print("=[indego.alerts[0]]====")
        #print(indego.alerts[0])
        #print("=[indego.alerts[1]]====")
        #print(indego.alerts[1])
        #print("=[indego.alerts[2]]====")
        #print(indego.alerts[2])
        #print("=[indego.alerts[3]]====")
        #print(indego.alerts[3])

        # Wakes mower!
        # print(" ")
        # print("=[indego.update_config]====")
        # indego.update_config()
        # print(indego.config)

        #print(" ")
        #print("=[indego.update_generic_data]====")
        #indego.update_generic_data()
        #print(indego.generic_data)
        #print("Generic data min voltage: ", indego.generic_data.model_voltage.min)
        #print(indego.generic_data.alm_mode)

        print(" ")
        print("=[indego.update_last_mow]====")
        indego.update_last_completed_mow()
        print(indego.last_completed_mow)

        #print(" ")
        #print("=[update_location]====")
        #indego.update_location()
        #print(indego.location)

        # print(" ")
        # print("=[indego.update_network]===")
        # indego.update_network()
        # print(indego.network)

        #print(" ")
        #print("=[indego.update_next_mow]===")
        #indego.update_next_mow()
        #print(indego.next_mow)
        
        # Wakes mower!
        # # print(" ")
        # print("=[operating data]====")
        # indego.update_operating_data()
        # print(indego.operating_data)
#
        #print(" ")
        #print("=[indego.update_security]===")
        #indego.update_security()
        #print(indego.security)

        # Wakes mower!
        # print(" ")
        # print("=[indego.update_setup]===")
        # indego.update_setup()
        # print(indego.setup)

        #print(" ")
        #print("=[updates]====")
        #indego.update_updates_available()
        #print(indego.update_available)
        
        #print(" ")
        #print("=[user]====")
        #indego.update_user()
        #print(indego.user)


if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    
    for i in range(10):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"=[{current_time}]=================================================================================================")
        print(f"Iteration:  {i+1}")
        main(config)

        print(f"End iteration:  {i+1}")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"=[{current_time}]=================================================================================================")
        print(" ")
        print("Sleep for 60 seconds")

        time.sleep(60)
