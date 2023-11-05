#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import json
from pyIndego import IndegoClient

logging.basicConfig(filename="pyIndego.log", level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

def main(config):
    """example of how to instantiate a indego object and get the schedule information"""
    with IndegoClient(**config) as indego:
        indego.update_predictive_schedule()

        print("Times where SmartMowing is planing to mow the lawn:")

        if indego.predictive_schedule is not None:
            for i in range(datetime.now().weekday(), datetime.now().weekday()+7):
                for j in range(len(indego.predictive_schedule.schedule_days)):
                    if (indego.predictive_schedule.schedule_days[j].day == (i % 7)):
                        print("\t{}".format(indego.predictive_schedule.schedule_days[j].day_name))
                        for k in range(len(indego.predictive_schedule.schedule_days[j].slots)):
                            print('\t\t{:%H:%M} - {:%H:%M}'.format(indego.predictive_schedule.schedule_days[j].slots[k].start, indego.predictive_schedule.schedule_days[j].slots[k].end))

            print("Times that are excluded for mowing from SmartMowing:")

            for i in range(datetime.now().weekday(), datetime.now().weekday()+7):
                for j in range(len(indego.predictive_schedule.exclusion_days)):
                    if (indego.predictive_schedule.exclusion_days[j].day == (i % 7)):
                        print("\t{}".format(indego.predictive_schedule.exclusion_days[j].day_name))
                        for k in range(len(indego.predictive_schedule.exclusion_days[j].slots)):
                            print('\t\t{:%H:%M} - {:%H:%M} {}'.format(indego.predictive_schedule.exclusion_days[j].slots[k].start, indego.predictive_schedule.exclusion_days[j].slots[k].end, indego.predictive_schedule.exclusion_days[j].slots[k].Attr))
        else:
            print("Error getting predictive schedule info")

if __name__ == "__main__":
    with open("config.json", "r",encoding="utf-8") as config_file:
        _config = json.load(config_file)
    main(_config)
