[![PyPI](https://img.shields.io/pypi/v/pyIndego.svg)](https://pypi.python.org/pypi/pyIndego/)

# API for the Bosch Indego lawnmowers

## Usage with Home Assistant
For source files and version handling: https://github.com/jm-73/pyIndego

For PYPI package: https://pypi.org/project/pyIndego/

## Basic information needed

Information   | Description
--------------|------------
your_username | Your username in the BoschSmartMove app
your_password | Your password for the app
your_serial   | Your Bosch Indego serial (found on the mover, in the mover menu or in the app)

The python library is written for the login method with username (email address) and password. Login with Facebook account is not supported.

## Call the API and the mower
Call the API:

    IndegoApi_Instance = IndegoAPI(username=your_mail@gmail.com, password=your_password, serial=your_serial)

## get-functions
Description for the functions updating data from API and mower. The functions collecting data from only Bosch API does not wake up mower. Functions collecting data from both Bosch API and mower does wake up mower from sleeping.

API Call         | Bosch API | Mower | Mower needs to be online
-----------------|-----------|-------|-------------------------
getAlerts        |           |       |
getGenericData   |           |       |
getNextCutting   |           |       |
getOperatingData |    X      |  X    |   X
getState         |    X      |       |
getUpdates       |           |       |   X
getUsers         |           |       |
login            |    X      |       |

## List of get-functions

### getAlerts()
Collect alerts.

```python
Response:
{
    'alm_sn': '123456789', 
    'alert_id': '5d48171263c5345a75dbc017', 
    'error_code': 'ntfy_blade_life', 
    'headline': 'Underhållstips.', 
    'date': '2019-08-05T11:46:26.397Z', 
    'message': 'Kontrollera klippknivarna. Indego har klippt i 100 timmar. Ska den fungera optimalt, kontrollera klippknivarna så att de är i bra skick. Du kan beställa nya knivar via avsnittet Tillbehör.', 
    'read_status': 'unread', 
    'flag': 'warning', 
    'push': True
}
```

### getGenericData()
Collect serial, service counter, name, mowing mode, model number and firmware.

```python
Response:
{
    'alm_sn': '123456789', 
    'alm_name': 'Indego', 
    'service_counter': 60488, 
    'needs_service': False, 
    'alm_mode': 'manual', 
    'bareToolnumber': '3600HA2300', 
    'alm_firmware_version': '00837.01043'
}
```

### getNextcutting()
Collects data on next cutting. Seems to get the last command sent to the mower.

```python
Response:
{
    'lastMowSent': '2019-08-20T05:09:51.842+01:00',
    'lastMowCode': 200
}
```

### getOperatingData()
Collect operational data data: battery, runtime, garden data and temperature.

```python
Response:
{
    'runtime': {
        'total': {
            'operate': 86333, 
            'charge': 25845
        }, 
        'session': {
            'operate': 0, 
            'charge': 0
        }
    }, 
    'battery': {
        'voltage': 33.5, 
        'cycles': 1, 
        'discharge': 0.0, 
        'ambient_temp': 17, 
        'battery_temp': 17, 
        'percent': 335
    }, 
    'garden': {
        'id': 7, 
        'name': 1, 
        'signal_id': 1, 
        'size': 625, 
        'inner_bounds': 3, 
        'cuts': 26, 
        'runtime': 82197, 
        'charge': 24860, 
        'bumps': 4650, 
        'stops': 24, 
        'last_mow': 4
    }, 
    'hmiKeys': 1344
}
```

### getState()
Collects state of mower, % lawn mowed, position, runtime, map coordinates.

```python
Response:
{
    'state': 64513, 
    'map_update_available': True, 
    'mowed': 95, 
    'mowmode': 0, 
    'xPos': 68, 
    'yPos': 30, 
    'runtime': {
        'total': {
            'operate': 86327, 
            'charge': 25845
            }, 
        'session': {
            'operate': 4, 
            'charge': 0
            }
        }, 
    'mapsvgcache_ts': 1565381013023, 
    'svg_xPos': 928, 
    'svg_yPos': 264
}
```

### getUpdates()
Check if there are any updates apllicable to the mower.

```python
Response:
{
     'available': False
}
```

### getUsers()
Collect user data.

```python
Response:
{
    'email': 'mail@gmail.com', 
    'display_name': 'Indego', 
    'language': 'sv', 
    'country': 'GB', 
    'optIn': True, 
    'optInApp': True
}
```



## Functions for reading data from locally cached API data
All functions that doesnt contain "get" first in name is collecting data from locally stored variables. No API calls to Bosch or mower.

### AlertsCount()
![Alertscount](https://img.shields.io/badge/Needs-getAlert-red)<br>
Counts the current alarms on mower.

```python
Response:
1
```

### AlertsDescription()
![AlertDescription](https://img.shields.io/badge/Needs-getAlert-red)<br>
Get detailed list of alerts

```python
Response:
[
    {
        'alm_sn': '505703041', 
        'alert_id': '5d5c395c63c5346994440e60', 
        'error_code': 'ntfy_blade_life', 
        'headline': 'Underhållstips.', 
        'date': '2019-08-20T18:18:04.472Z', 
        'message': 'Kontrollera klippknivarna. Indego har klippt i 100 timmar. Ska den fungera optimalt, kontrollera klippknivarna så att de är i bra skick. Du kan beställa nya knivar via avsnittet Tillbehör.', 
        'read_status': 'unread', 
        'flag': 'warning', 
        'push': True
    } 
]
```

### AlmFirmwareVersion()
![Alertscount](https://img.shields.io/badge/Needs-getGenericData-red)<br>
Gets the mower firmware version.

```python
response:
smart
```

### AlmMode()
![Alertscount](https://img.shields.io/badge/Needs-getGenericData-red)<br>
Gets the mower mode.

```python
response:
smart
```

### AlmName()
![Alertscount](https://img.shields.io/badge/Needs-getGenericData-red)<br>
Gets the mower instance name.
```python
response:
Indego
```


### BareToolNumber() 
![Alertscount](https://img.shields.io/badge/Needs-getGenericData-red)<br>
Show the model number of the mower.

```python
Response:
3600HA2300
```

### Battery()
![Alertscount](https://img.shields.io/badge/Needs-getOperatingData-red)<br>
Get battery information.
```python
Response:
???
```

### BatteryPercent()
![Alertscount](https://img.shields.io/badge/Needs-getOperatingData-red)<br>
Get the raw value for percentage left. For Gen 1 this seems to be the battery voltage. For Gen 2 mowers it seems to be the actual percentage left in the battery.
```python
Response:
???
```

### BatteryPercentAdjusted()
![Alertscount](https://img.shields.io/badge/Needs-getOperatingData-red)<br>
Get the adjusted value for percentage left. Calculated for Gen 1 mowers, and the actual percentage value for Gen 2.
```python
Response:
85
```

### BatteryVoltage()
![Alertscount](https://img.shields.io/badge/Needs-getOperatingData-red)<br>
Get the voltage for the battery. For Gen 1 mowers this value seems to be correct. For Gen 2 it seems to be the same value as the percentage left in battery.
```python
Response:
38.6
```

### BatteryCycles()
![Alertscount](https://img.shields.io/badge/Needs-getOperatingData-red)<br>
Dont know what this value is?
```python
Response:
0
```

### BatteryDischarge()
![Alertscount](https://img.shields.io/badge/Needs-getOperatingData-red)<br>
Seems to be the Ah the mower is currently drawing.
```python
Response:
1.2
```

### BatteryAmbientTemp()
![Alertscount](https://img.shields.io/badge/Needs-getOperatingData-red)<br>
Seems to be the ambient temp of the battery.
```python
Response:
28
```

### BatteryTemp()
![Alertscount](https://img.shields.io/badge/Needs-getOperatingData-red)<br>
Seems to be the temp of the battery.
```python
Response:
29
```

### Country()
![Alertscount](https://img.shields.io/badge/Needs-getUsers-red)<br>
Show country for the Bosch account.
```python
Response:
GB
```

### Displayname()
![Alertscount](https://img.shields.io/badge/Needs-getUsers-red)<br>
Show name for the Bosch account.
```python
Response:
mowername
```

### Email()
![Alertscount](https://img.shields.io/badge/Needs-getUsers-red)<br>
Show email adress for the Bosch account.
```python
Response:
mail@gmail.com
```

### FriendlyAlertErrorCode()
![Alertscount](https://img.shields.io/badge/Needs-getAlert-red)<br>
Get user friendly alert error code description to be shown in HA GUI.
```python
Response:
Reminder blade life
```

### Garden()
![Alertscount](https://img.shields.io/badge/Needs-getOperatingData-red)<br>
Dont know what this is?
```python
Response:
{
    'garden': {
        'id': 7, 
        'name': 1, 
        'signal_id': 1, 
        'size': 625, 
        'inner_bounds': 3, 
        'cuts': 26, 
        'runtime': 82197, 
        'charge': 24860, 
        'bumps': 4650, 
        'stops': 24, 
        'last_mow': 4
    }
} 
```

### HmiKeysn()
![Alertscount](https://img.shields.io/badge/Needs-getOperatingData-red)<br>
Dont know what this is?
```python
Response:
1344
```

### Language
![Alertscount](https://img.shields.io/badge/Needs-getUsers-red)<br>
Show language for the Bosch account.
```python
Response:
sv
```

### MapSvgCacheTs()
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Dont know what this is...
```python
Response:
1565416077642
```

### MapUpdateAvailable()
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Show if there is an update of the map image.
```python
Response:
True
```

### ModelDescription()
Need: getxxx. Get user friendly model name.

```python
response:
Indego Connect 1000
```

### ModelVoltage()
Need: getxxx. Get the predefined voltage limits in order to calculate battery percentage.

```python
response:
{
    'min': '297',
    'max': '369'
}
```

### ModelVoltageMin()
Need: getxxx. Get the minimum predefined voltage limits in order to calculate battery percentage.

```python
response:
297
```

### ModelVoltageMin()
Need: getxxx. Get the maximum predefined voltage limits in order to calculate battery percentage.

```python
response:
369
```


### Mowed() 
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Show percentage of lawn mowed
```python
Response:
95
```

### MowerState()
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Show current state of mower
```python
Response:
258
```

### MowerStateDescription()
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Show simple description of current state of mower. States available are Docked, Mowing, Stuck, Diagnostics mode, End of life, Software update.
```python
Response:
Docked
```

### MowerStateDescriptionDetailed()
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Show description in detail of current state of mower.

```python
Response:
Sleeping
```

### MowingModeDescription()
Need: getxxx. Get the user friendly mowing mode description.

```python
response:
Smart
```

### NeedsService()
![Alertscount](https://img.shields.io/badge/Needs-getGenericData-red)<br>
Gets the needs service flag. Dont know when it is used.

```python
Response:
False
```

### NextCutting()
Need: get???. Should get the next planned cutting session. Seems to give the last sent mower command.
```python
Response:
{
    'lastMowSent': '2019-08-20T05:09:51.842+01:00', 
    'lastMowCode': 200
}
```

### OptIn()
![Alertscount](https://img.shields.io/badge/Needs-getUsers-red)<br>
Dont know what this are for?
```python
Response:
True
```

### OptInApp()
![Alertscount](https://img.shields.io/badge/Needs-getUsers-red)<br>
Dont know what this are for?
```python
Response:
True
```

### Runtime()
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Get session and total rutime and charge time in minutes.
```python
Response:
{
    'total': {
        'operate': 86389, 
        'charge': 25891
    }, 
    'session': {
        'operate': 0, 
        'charge': 0
    }
}
```

### RuntimeSession()
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Get session runtime and charge time in minutes
```python
Response:
{
    'operate': 4, 
    'charge': 1
}
```

### RuntimeTotal()
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Get total runtime and charge time in hours
```python
response:
{
    'operate': 86389, 
    'charge': 25891
}
```

### Serial()
Get the serial number
```python
response:
123456789
```

### ServiceCounter()
Get service counter for knives
```python
response:
73275
```

### SvgxPos())
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Show svg x-position of mower.
```python
Response:
928
```

### FirmwareAvailable())
Need: get???. ???

```python
Response:
false
```

### SvgyPos()) ***
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Show svg y-position of mower.
```python
Response:
264
```

### xPos())
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Show x-position of mower.
```python
Response:
85
```

### yPos()) ***
![Alertscount](https://img.shields.io/badge/Needs-getState-red)<br>
Show y-position of mower.
```python
Response:
48
```

## Sending commands

### putCommand(command)
Send command. Accepted commands:

Command     |Description         
------------|--------------------
mow         |Start mowing        
pause       |Pause mower         
returnToDock|Return mower to dock


## Not working

### Not properly implemented yet

    getLocation()
Get garden location (GPS coordinates?)

    getPredicitiveCalendar()
Get the calender for predicted cutting sessions

    getUserAdjustment()
Get the user adjustment of the cutting frequency

    getCalendar()
Get the calendar for allowed cutting times

    getSecurity()
Get the security settings

    getAutomaticUpdate()
Get the automatic update settings


# API CALLS
https://api.indego.iot.bosch-si.com:443/api/v1


```python
get
/authenticate
/alerts
/alms/<serial>
/alms/<serial>/automaticUpdate
/alms/<serial>/updates
/alms/<serial>/calendar
/alms/<serial>/map
/alms/<serial>/operatingData
/alms/<serial>/predictive/nextcutting?withReason=true
/alms/<serial>/predictive/nextcutting?last=YYYY-MM-DDTHH:MM:SS%2BHH:MM (Not working)
/alms/<serial>/predictive/location
/alms/<serial>/predictive/calendar
/alms/<serial>/predictive/useradjustment (What is this for?)
/alms/<serial>/security
/alms/<serial>/state

put
```