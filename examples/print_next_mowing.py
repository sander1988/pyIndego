#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timezone, timedelta
from pyIndego import IndegoClient

def main(config):
    with IndegoClient(**config) as indego:
        
        indego.update_next_mow()
        print("Next mowing:", indego.next_mow)
        
        nowDate = datetime.now(timezone.utc)
        if (indego.next_mow - nowDate) < timedelta(hours=2, minutes=30):
            print("Less than two and a half hours before mowing.")

if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    main(config)
