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

API Call         | Bosch API | Mower
-----------------|-----------|-------
getAlerts        |           |
getGenericData   |           |
getNextCutting   |           |
getOperatingData |    X      |  X
getState         |    X      |
getUpdates       |           |
getUsers         |           |
login            |    X      |

## List of get-functions

### getAlerts()
Collect alerts.

```python
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

### getNextcutting()
Collects data on next cutting. (Not implemented yet)

### getOperatingData()
Collect operational data data: battery, runtime, garden data and temperature.

```python
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
 {'available': False}
```

### getGenericData()
Collect serial, service counter, name, mowing mode, model number and firmware.

```python
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

### getUsers()
Collect user data.

```python
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

### getAlertsDescription()
Need: getAlert. Get detailed list of alerts

### getBatteryInformation()
Get detailed battery information

### Country()
Need getUsers. Show country for the Bosch account.
```python
Response:
mowername
```

### Displayname()
Need getUsers. Show name for the Bosch account.
```python
Response:
mowername
```

### Email()
Need getUsers. Show email adress for the Bosch account.

```python
Response:
mail@gmail.com
```

### getFirmware()
Get the mower firmware version

### Language
Need getUsers. Show language for the Bosch account.
```python
Response:
sv
```

### MapSvgCacheTs() ***
Need: getState. Dont know what this is...

```python
Response:
1565416077642
```

### MapUpdateAvailable() **
Need: getState. Show if there is an update of the map image.

```python
Response:
True
```

### getModel()
Get the mower model

### Mowed() **
Need: getState. Show percentage of lawn mowed

```python
Response:
95
```

### MowerState() ***
Need: getState. Show current state of mower

```python
Response:
258
```

### MowerStateDescription() ***
Need: getState. Show description of current state of mower

```python
Response:
Docked
```

### MowMode() ***
Need: getState. Not working, use alm_mode instead!

```python
Response:
0
```

### getNeedsService()
Get the change knives flag

```python
Response:
```

### getOptIn()
Need: getUSers. ???

```python
Response:
True
```

### getOptInApp()
Need: getUSers. ???

```python
Response:
True
```


### getPosition()
Get position (relative on map)

### Runtime() ***
Need: getState. Get session and total rutime and charge time in minutes
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

### RuntimeSession() ***
Need: getState. Get session runtime and charge time in minutes

```python
{
    'operate': 4, 
    'charge': 1
}
```

### RuntimeTotal() ***
Need: getState. Get total runtime and charge time in hours

```python
{
    'operate': 86389, 
    'charge': 25891
}

### getSerial()
Get the serial number

### getServiceCounter()
Get service counter for knives

### SvgxPos()) ***
Need: getState. Show svg x-position of mower.

```python
Response:
928
```

### SvgyPos()) ***
Need: getState. Show svg y-position of mower.

```python
Response:
264
```

### getUpdateAvailable()
Check if there is an update available

### getUpdateAvailable()
Get the user data.

```python
Response:
```

### xPos()) ***
Need: getState. Show x-position of mower.

```python
Response:
85
```

### yPos()) ***
Need: getState. Show y-position of mower.

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
    getName()
NOT WORKING (Not implemented by Bosch?)
Get the mower name

    getNextPredicitiveCutting()
NOT WORKING! (No data returned from API)
Get next scheduled cutting session

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