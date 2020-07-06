import json
import logging

from pyIndego import IndegoClient

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
        # print("=[indego.update_all]====")
        # indego.update_all(force=True)
        # print(indego)

        # print(" ")
        print("=[indego.update_alerts]====")
        indego.update_alerts()
        print(indego.alerts)
        print("=[indego.alerts_count]====")
        print(indego.alerts_count)
        print("=[indego.alerts[0]]====")
        print(indego.alerts[0])
        print("=[indego.alerts[1]]====")
        print(indego.alerts[1])
        print("=[indego.alerts[2]]====")
        print(indego.alerts[2])
        print("=[indego.alerts[3]]====")
        print(indego.alerts[3])

        # print(" ")
        # print("=[indego.update_generic_data]====")
        # indego.update_generic_data()
        # print(indego.generic_data)
        # print("Generic data min voltage: ", indego.generic_data.model_voltage.min)
        # print(indego.generic_data.alm_mode)
        # print(indego.alm_name)

        # print(" ")
        # print("=[indego.update_last_completed_mow]====")
        # indego.update_last_completed_mow()
        # print(indego.last_completed_mow)

        # print(" ")
        # print("=[update_location]====")
        # indego.update_location()
        # print(indego.location)

        # print("=[longpoll_state]====")
        # indego.update_longpoll_state(40)
        # print(indego.longpoll_state)

        # indego.update_network()
        # print(indego.network)
        # indego.update_all(force=True)
        # print(indego)
        # print("=[state]====")
        # indego.update_state()
        # print(indego.state)

        print(" ")
        print("=[alerts]====")
        indego.update_alerts()
        print(indego.alerts)
        print("=[alerts_count]====")
        print(indego.alerts_count)

        print(" ")
        print("=[generic_data]====")
        indego.update_generic_data()
        print(indego.generic_data)

        print(" ")
        print("=[last_completed_mow]====")
        indego.update_last_completed_mow()
        print(indego.last_completed_mow)

        print(" ")
        print("=[location]====")
        indego.update_location()
        print(indego.location)

        # print("=[longpoll_state]====")
        # indego.update_longpoll_state(40)
        # print(indego.longpoll_state)

        print(" ")
        print("=[operating data]====")
        indego.update_operating_data()
        print(indego.operating_data)

        # indego.update_network()
        # print(indego.network)

        # print(" ")
        # print("=[indego.update_next_mow]===)
        # indego.update_next_mow()
        # indego.update_operating_data()
        # # indego.update_updates()
        # # indego.update_user
        # # indego.update_network()

        print("=[updates]====")
        indego.update_updates_available()
        print(indego.update_available)
        print(" ")
        print("=[user]====")
        indego.update_user()
        print(indego.user)
        # indego.update_network()

        # indego.download_map()

        # print("map: ", indego.map_filename)
        # print("network ", indego.network)
        # print("state: ", indego.state)
        # print("user: ", indego.user)
        # print("Generic data: ", indego.generic_data)
        # print("Generic data min voltage: ", indego.generic_data.model_voltage.min)
        # print("Alerts: ", indego.alerts)
        # print("Operating_data: ", indego.operating_data)
        # print("Battery: ", indego.operating_data.battery)
        # print("Battery percent: ", indego.operating_data.battery.percent_adjusted)
        # print("Battery voltage: ", indego.operating_data.battery.voltage)

        # print(" ")
        # print("=[indego.update_security]===")
        # indego.update_security()
        # print(indego.security)

        # print(" ")
        # print("=[indego.update_setup]===")
        # indego.update_setup()
        # print(indego.setup)

        # print(" ")
        # print("=[indego.update_state]===")
        # indego.update_state()
        # print(indego.state)
        # print("=[update_state longloll]===")
        # indego.update_state(longpoll=True, longpoll_timeout=20)
        # print(indego.state)

        # print(" ")
        # print("=[indego.update_updates_available]====")
        # indego.update_updates_available()
        # print(indego.update_available)

        # print(" ")
        # print("=[indego.update_users]====")
        # indego.update_users()
        # print(indego.users)

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
        # print(indego.email)
        # print(indego.garden)
        # print(indego.x_pos, ", ", indego.y_pos)
        # indego.show_vars()


if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    main(config)
