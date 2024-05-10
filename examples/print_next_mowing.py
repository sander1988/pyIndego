#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime, timezone, timedelta
from pyIndego import IndegoClient

logging.basicConfig(filename="pyIndego.log", level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

def main(config):
    """example of how to instantiate a indego object and get the mowing time"""
    with IndegoClient(**config) as indego:

        indego.update_next_mow()
        print("Next mowing:", indego.next_mow)

        now_date = datetime.now(timezone.utc)
        if indego.next_mow is not None:
            if (indego.next_mow - now_date) < timedelta(hours=2, minutes=30):
                print("Less than two and a half hours before mowing.")
        else:
            print("Error getting mowing time")

if __name__ == "__main__":
    with open("config.json", "r", encoding="utf-8") as config_file:
        _config = json.load(config_file)
    main(_config)
