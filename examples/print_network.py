#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from pyIndego import IndegoClient

logging.basicConfig(filename="pyIndego.log", level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

def country_operator(mcc, mnc):
    """get the country and network operator from network ID's"""
    if mcc == 262:
        country =  "Germany"
        if mnc == 1:
            operator = "Telekom Deutschland"
        elif mnc == 2:
            operator = "Vodafone"
        elif mnc == 3:
            operator = "Telefónica"
        else:
            operator = None
    elif mcc == 232:
        country =  "Austria"
        if mnc == 1:
            operator = "A1 Telekom Austria"
        elif mnc == 2:
            operator = "Magenta Telekom"
        elif mnc == 5:
            operator = "Hutchison Drei Austria"
    elif mcc == 228:
        country =  "Switzerland"
        if mnc == 1:
            operator = "Swisscom"
        elif mnc == 2:
            operator = "Sunrise Communications"
        elif mnc == 3:
            operator = "Salt Mobile SA"
        else:
            operator = None
    else:
        country = None
        operator = None
    return (country, operator)


def main(config):
    """example of how to instantiate a indego object and get the network info"""
    with IndegoClient(**config) as indego:
        indego.update_network()

        if indego.network is not None:
            (country, operator) = country_operator(indego.network.mcc, indego.network.mnc)
            if country is not None:
                print("Country is:", country)
                if operator is not None:
                    print("Operator is:", operator)
                else:
                    print("Operator is unknown")
            else:
                print("Country and operator are unknown")

            print("Signal strength (rssi):", indego.network.rssi)

            print("Available Networks:")
            for i in range(indego.network.networkCount):
                (country, operator) = country_operator(int(str(indego.network.networks[i])[:3]), int(str(indego.network.networks[i])[3:5]))
                if (country is not None) and (operator is not None):
                    print("\t", country, ":", operator)
                else:
                    print("\tmcc =", str(indego.network.networks[i])[:3], ": mnc =", str(indego.network.networks[i])[3:5])
        else:
            print("Error getting network info")

if __name__ == "__main__":
    with open("config.json", "r",encoding="utf-8") as config_file:
        _config = json.load(config_file)
    main(_config)
