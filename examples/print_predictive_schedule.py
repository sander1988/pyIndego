#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import json
from pyIndego import IndegoClient

def main(config):
    with IndegoClient(**config) as indego:
        indego.update_predictive_schedule()
        
        print("Times where SmartMowing is planing to mow the lawn:")
        
        for i in range(len(indego.predictive_schedule.schedule_days)):
            print("\t{}".format(indego.predictive_schedule.schedule_days[i].day_name))
            for j in range(len(indego.predictive_schedule.schedule_days[i].slots)):
                print('\t\t{:%H:%M} - {:%H:%M}'.format(indego.predictive_schedule.schedule_days[i].slots[j].start, indego.predictive_schedule.schedule_days[i].slots[j].end))

        print("Times that are excluded for mowing from SmartMowing:")
        
        for i in map(lambda x : x + datetime.now().weekday(), range(len(indego.predictive_schedule.exclusion_days))):
            print("\t{}".format(indego.predictive_schedule.exclusion_days[i % 7].day_name))
            for j in range(len(indego.predictive_schedule.exclusion_days[i % 7].slots)):
                print('\t\t{:%H:%M} - {:%H:%M} {}'.format(indego.predictive_schedule.exclusion_days[i % 7].slots[j].start, indego.predictive_schedule.exclusion_days[i % 7].slots[j].end, indego.predictive_schedule.exclusion_days[i % 7].slots[j].Attr))

if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    main(config)
