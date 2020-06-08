[![PyPI](https://img.shields.io/pypi/v/pyIndego)](https://pypi.python.org/pypi/pyIndego/)

# API for Bosch Indego lawnmowers

Join the Discord channel to discuss around this integration:
https://discord.gg/aD33GsP

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

    IndegoApi_Instance = IndegoAPI(username='your_mail@gmail.com', password='your_password', serial='your_serial')

## get-functions
Description for the functions updating data from API and mower. The functions collecting data from only Bosch API does not wake up mower. Functions collecting data from both Bosch API and mower does wake up mower from sleeping.

API Call                 | Bosch API | Mower | Mower needs to be online
-------------------------|-----------|-------|-------------------------
getAlerts                |    X      |       |
getGenericData           |    X      |       |
getLastComletedCutting   |    X      |       |
getOperatingData         |           |  X    |   X
getState                 |    X      |       |
getUpdates               |           |  X    |   X
getUsers                 |    X      |       |
login                    |    X      |       |

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

### getLastCutting()
Collects data on the last completed mow. .

```python
Response:
{
    'mow_next': '2020-05-25T10:00:00+02:00'
}
```

### getLocation()
Collect location of the garden/mower.

```python
Response:
{
    'latitude': '59.742950', 
    'longitude': '17.380440', 
    'timezone': 'Europe/Berlin'
}
```

### getNextCutting()
Collects data on next cutting. Returns none if mower is set to manual mode.

```python
Response:
{
    'mow_next': '2020-05-25T10:00:00+02:00'
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
All functions that doesnt contain "get" first in name is collecting data from locally stored variables in the function. No API calls to Bosch or mower.

### AlertsCount()  Counts the current alarms on mower.
### AlertsDescription() Get detailed list of alerts
### AlmFirmwareVersion() Gets the mower firmware version.
### AlmMode() Gets the mower mode.
### AlmName() Gets the mower instance name.
### BareToolNumber() Show the model number of the mower.
### Battery() Get battery information.
### BatteryAmbientTemp() Seems to be the ambient temp of the battery.
### BatteryCycles() Dont know what this value is?
### BatteryDischarge() Seems to be the Ah the mower is currently drawing.### BatteryPercent() Get the raw value for percentage left. For Gen 1 this seems to be the battery voltage. For Gen 2 mowers it seems to be the actual percentage left in the battery.
### BatteryPercentAdjusted() Get the adjusted value for percentage left. Calculated for Gen 1 mowers, and the actual percentage value for Gen 2.
### BatteryTemp() Seems to be the temp of the battery.
### BatteryVoltage() Get the voltage for the battery. For Gen 1 mowers this value seems to be correct. For Gen 2 it seems to be the same value as the percentage left in battery.
### ConvertBoschDateTime() Convert Bosch abbreviation for time to std 24h time
### Country() Show country for the Bosch account.
### Displayname() Show name for the Bosch account.
### Email() Show email adress for the Bosch account.
### FirmwareAvailable() Checks if there are any firmware updates available for the mower.
### FriendlyAlertErrorCode() Get user friendly alert error code description to be shown in HA GUI.
### Garden() Dont know what this is?
### HmiKeysn() Dont know what this is?
### Language() Show language for the Bosch account.
### MapSvgCacheTs() Dont know what this is...
### MapUpdateAvailable() Show if there is an update of the map image.
### ModelDescription() Get user friendly model name.
### ModelVoltage() Get the predefined voltage limits in order to calculate battery percentage.
### ModelVoltageMax() Get the maximum predefined voltage limits in order to calculate battery percentage.
### ModelVoltageMin() Get the minimum predefined voltage limits in order to calculate battery percentage.
### MowMode() Show mowers mow mode
### Mowed() Show percentage of lawn mowed
### MowerState() Show current state of mower
### MowerStateDescription() Show simple description of current state of mower. States available are Docked, Mowing, Stuck, Diagnostics mode, End of life, Software update.
### MowerStateDescriptionDetailed() Show description in detail of current state of mower.
### MowingModeDescription() Get the user friendly mowing mode description.
### NeedsService() Gets the needs service flag. Dont know when it is used.
### NextCutting() Should get the next planned cutting session.
### OptIn() Dont know what this are for?
### OptInApp() Dont know what this are for?
### Runtime() Get session and total rutime and charge time in minutes.
### RuntimeSession() Get session runtime and charge time in minutes
### RuntimeTotal() Get total runtime and charge time in hours
### Serial() Get the serial number
### ServiceCounter() Get service counter for knives
### SvgxPos() Show svg x-position of mower.
### SvgyPos() Show svg y-position of mower.
### xPos() Show x-position of mower.
### yPos() Show y-position of mower.

## Sending commands

### putCommand(command)
Send command. Accepted commands:

Command     |Description         
------------|--------------------
mow         |Start mowing        
pause       |Pause mower         
returnToDock|Return mower to dock

### putMowMode(command)
Send command. Accepted commands:

Command     |Description         
------------|--------------------
true        |Smart Mow enabled        
false       |Smart Mow disabled   

## Not working

### Not properly implemented yet

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
post
/authenticate

get
/alerts
/alms/<serial>
/alms/<serial>/automaticUpdate
/alms/<serial>/calendar
/alms/<serial>/map
/alms/<serial>/updates
/alms/<serial>/operatingData
/alms/<serial>/predictive
/alms/<serial>/predictive/calendar
/alms/<serial>/predictive/lastcutting
/alms/<serial>/predictive/location
/alms/<serial>/predictive/nextcutting
/alms/<serial>/predictive/useradjustment
/alms/<serial>/predictive/weather
/alms/<serial>/security
/alms/<serial>/state
/users/<userid>

put
/alms/<serial>/automaticUpdate
/alms/<serial>/predictive/calendar
/alms/<serial>/predictive/location
/alms/<serial>/predictive
/alms/<serial>/state
/alms/<serial>/predictive/useradjustment

delete
/alerts/<alertid>
```