[![PyPI](https://img.shields.io/pypi/v/pyIndego)](https://pypi.python.org/pypi/pyIndego/)

# API for Bosch Indego lawnmowers

Join the Discord channel to discuss around this integration:
https://discord.gg/aD33GsP

## Usage with Home Assistant
For source files and version handling: https://github.com/jm-73/pyIndego

For PYPI package: https://pypi.org/project/pyIndego/

## Basic information needed

The library requires python 3.7 or above.

Information   | Description
--------------|------------
your_username | Your username in the BoschSmartMove app
your_password | Your password for the app
your_serial   | Optional: Your Bosch Indego serial (found on the mover, in the mover menu or in the app)

This library is written for the login method with username (email address) and password. Login with Facebook account is not supported.

## Call the API and the mower
Call the API, synchronously:

    from pyIndego import IndegoClient
    indego = IndegoClient(username='your_mail@gmail.com', password='your_password', serial='your_serial')

Call the API, asynchronously:

    from pyIndego import IndegoAsyncClient
    indego = IndegoAsyncClient(username='your_mail@gmail.com', password='your_password', serial='your_serial')

    await indego.close()

## Properties
### indego.serial
Returns the serial number of the indego mower, is usefull mostly when serial was not initialized.

### indego.state_description
Returns a description of the state, instead of a number.

### indego.state_description_detail
Returns a detailed description of the state, instead of a number.

### indego.next_mows


## Update/download functions
Description for the functions updating data from API and mower. The functions collecting data from only Bosch API does not wake up mower. Functions collecting data from both Bosch API and mower does wake up mower from sleeping.

Call                               | Bosch API | Mower | Mower needs to be online
-----------------------------------|-----------|-------|-------------------------
indego.update_alerts()             |    X      |       |
indego.update_all()                |           |       |
indego.update_calendar()           |    X      |       |
indego.update_config()             |           |       |
indego.update_generic_data()       |    X      |       |
indego.update_last_completed_mow() |    X      |       |
indego.update_location()           |           |       |
indego.update_network()            |    ?      |  ?    |   ?
indego.update_next_mow()           |           |       |
indego.update_operating_data()     |           |  X    |
indego.update_predictive_calendar()|    X      |       |
indego.update_predictive_schedule()|    X      |       |
indego.update_security()           |    X      |       |
indego.update_setup()              |    X      |       |
indego.update_state()              |    X      |       |
indego.update_state(force=True)    |    X      |  X    |
indego.update_state(longpoll=True, longpoll_timeout=120)|X|  X    |
indego.update_updates_available()            |           |  X    |
indego.update_users()              |    X      |       |
indego.download_map(filename='')|||

### To be implemented
Predictive Setup

## List of update functions

### indego.update_all()
Updates all sensors.

### indego.update_alerts()
Updates alerts from API to indego.alerts.

```python
indego.alert_count = 1
[Alerts(alert_id='5d48171263c5345a75dbc017', error_code='ntfy_blade_life', headline='Underhållstips.', date='2019-08-05T11:46:26.397Z', message='Kontrollera klippknivarna. Indego har klippt i 100 timmar. Ska den fungera optimalt, kontrollera klippknivarna så att de är i bra skick. Du kan beställa nya knivar via avsnittet Tillbehör.', read_status='unread', flag='warning', push=True, alert_description='Reminder blade life')]
```

### indego.update_calendar()
Updates the calendar with the next planned mows.

```python
Calendar(cal=3, days=[CalendarDay(day=0, day_name='monday', slots=[CalendarSlot(En=True, StHr=10, StMin=0, EnHr=13, EnMin=0), CalendarSlot(En=False, StHr=None, StMin=None, EnHr=None, EnMin=None)]), CalendarDay(day=2, day_name='wednesday', slalendarSlot(En=False, StHr=None, StMin=None, EnHr=None, EnMin=None)])])
```

### indego.update_config()
Updates config to indego.config. With some Indegos, this function gives an error (e.g., Indego 1000), with others it works (e.g., Indego S+ 400).

```python
Config(region=0, language=1, border_cut=0, is_pin_set=True, wire_id=4, bump_sensitivity=0, alarm_mode=True)
```

### indego.update_generic_data()
Updates indego.generic_data with serial, service counter, name, mowing mode, model number and firmware version.

```python
GenericData(alm_name='Indego', alm_sn='505703041', service_counter=132436, needs_service=False, alm_mode='calendar', bareToolnumber='3600HA2300', alm_firmware_version='00837.01043', model_description='Indego 1000', model_voltage=ModelVoltage(min=297, max=369), mowing_mode_description='Calendar')
```

### indego.update_last_completed_mow()
Updates indego.last_completed_mow with date and time of the latest completed mow.

```python
indego.last_completed_mow = (DateTime) 2020-06-21 21:38:50.115000+02:00
```

### indego.update_location()
Updates indego.location with the location of the garden/mower.

```python
Location(latitude='59.742950', longitude='17.380440', timezone='Europe/Berlin')
```

### indego.update_network()
Updates data on the mobile network the Indego is connected to.

```python
Network(mcc=262, mnc=2, rssi=-77, currMode='s', configMode='s', steeredRssi=-100, networkCount=3, networks=[26201, 26202, 26203])
```

### indego.update_next_mow()
Updates the indego.next_mow with the next planned mow date and time.

```python
indego.next_mow = (DateTime) 2020-06-29 10:00:00+02:00
```

### indego.update_operating_data()
Update the indego.operating_data with data about battery, runtime, garden data and temperature.

```python
OperatingData(hmiKeys=1768, battery=Battery(percent=357, voltage=35.7, cycles=0, discharge=0.0, ambient_temp=26, battery_temp=26, percent_adjusted=83), garden=Garden(id=8, name=1, signal_id=1, size=769, inner_bounds=3, cuts=15, runtime=166824, charge=37702, bumps=6646, stops=29, last_mow=1, map_cell_size=None), runtime=Runtime(total=RuntimeDetail(operate=1715, charge=387, cut=1328), session=RuntimeDetail(operate=9, charge=0, cut=0)))
```

### indego.update_predictive_calendar()
Updates the predictive_calendar with the timeslots (days and hours) where the user wants smart mowing not to mow the lawn.

```python
PredictiveCalendar(cal=1, days=[CalendarDay(day=0, day_name='monday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr=None), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr=None)]), CalendarDay(day=1, day_name='tuesday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr=None), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr=None)]), CalendarDay(day=2, day_name='wednesday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr=None), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr=None)]), CalendarDay(day=3, day_name='thursday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr=None), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr=None)]), CalendarDay(day=4, day_name='friday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr=None), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr=None)]), CalendarDay(day=5, day_name='saturday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr=None), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr=None)]), CalendarDay(day=6, day_name='sunday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=23, EnMin=59, Attr=None)])])
```

### indego.update_predictive_schedule()
Updates the predictive_schedule with the next planned mows (schedule_days) and the days where the smart mowing will not mow the lawn. The latter is combined by the time slots where the user does not want the Indego to mow (Attr='C') and the slots where the weather conditions prevent the mowing (e.g., Attr='pP').

```python
PredictiveSchedule(schedule_days=[CalendarDay(day=0, day_name='monday', slots=[CalendarSlot(En=True, StHr=10, StMin=0, EnHr=13, EnMin=0, Attr=None)]), CalendarDay(day=2, day_name='wednesday', slots=[CalendarSlot(En=True, StHr=10, StMin=0, EnHr=13, EnMin=0, Attr=None)]), CalendarDay(day=4, day_name='friday', slots=[CalendarSlot(En=True, StHr=10, StMin=0, EnHr=13, EnMin=0, Attr=None)])], exclusion_days=[CalendarDay(day=0, day_name='monday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr='C'), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr='C')]), CalendarDay(day=1, day_name='tuesday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr='C'), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr='C')]), CalendarDay(day=2, day_name='wednesday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr='C'), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr='C')]), CalendarDay(day=3, day_name='thursday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr='C'), CalendarSlot(En=True, StHr=8, StMin=0, EnHr=12, EnMin=0, Attr='pP'), CalendarSlot(En=True, StHr=13, StMin=0, EnHr=15, EnMin=0, Attr='Pp'), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr='C')]), CalendarDay(day=4, day_name='friday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr='C'), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr='C')]), CalendarDay(day=5, day_name='saturday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr='C'), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr='C')]), CalendarDay(day=6, day_name='sunday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=23, EnMin=59, Attr='C')])])
```

### indego.update_security()
Updates the indego.security with information about the Indego security state.

```python
Security(enabled=True, autolock=False)
```

### indego.update_setup()
Updates the indego.setup with information if the Indego is set up.

```python
Setup(hasOwner=True, hasPin=True, hasMap=True, hasAutoCal=False, hasIntegrityCheckPassed=True)
```

### indego.update_state(force=False, longpoll=False, longpoll_timeout=120)
Updates the indego.state with state of mower, % lawn mowed, position, runtime, map coordinates.

If longpoll is set to True, it sends the latest state value to the server and then waits for the timeout to see if there are an updated state value. The server attempts to "hold open" (not immediately reply to) each HTTP request, responding and coming back only when there are events to deliver or the timeout (in seconds) is due.

This function can be used instead of polling the status every couple of seconds: place one longpoll status request with a timeout of max. 300 seconds and the function will provide its return value when the status has been updated. As soon as an answer is received, the next longpoll status request can be placed. This should save traffic on both ends.

```python
State(state=64513, map_update_available=True, mowed=78, mowmode=0, xPos=162, yPos=65, charge=None, operate=None, runtime=Runtime(total=RuntimeDetail(operate=1715, charge=387, cut=1328), session=RuntimeDetail(operate=5, charge=0, cut=0)), mapsvgcache_ts=1593207884109, svg_xPos=192, svg_yPos=544, config_change=None, mow_trig=None)
```

### indego.update_updates_available()
Check if there are any updates applicable to the mower and updates the (bool) `indego.update_available`.

### indego.update_users()
Updates the indego.users with information about the user.

```python
Users(email='youremail@mail.com', display_name='Indego', language='sv', country='SE', optIn=True, optInApp=True)
```

## Sending commands

### indego.delete_alert(alert_index)
Delete an alert from the list, index should exist. If this is called before update_alerts it will not work.

### indego.put_alert_read(alert_index)
Set the specified alert to read. This is a one way action, once read it is not possible to set back to unread. The function looks up the alert_id from indego.alerts, if it cannot find that ID or if update_alerts has not been run, this will stop and log a warning.

### indego.put_all_alerts_read()
Set all alerts to read, the function loops through the alert_id's from indego.alerts, if update_alerts has not been run, this will stop and log a warning.

### indego.put_command(command)
Send commands.

Command     |Description         
------------|--------------------
put_command('mow')          |Start mowing        
put_command('pause')        |Pause mower         
put_command('returnToDock') |Return mower to dock

### indego.put_mow_mode(command)
Send command. Accepted commands:

Command     |Description         
------------|--------------------
put_mow_mode('true')  |Smart Mow enabled        
put_mow_mode('false') |Smart Mow disabled   


## Not implemented yet

### update_ & put_predictive_setup()

```python
Response:
{
    'garden_size': 93,
    'mowing_duration': 3,
    'rain_factor': 1.4,
    'temperature_factor': 1.1,
    'garden_location': {
        'latitude': '48.7357',
        'longitude': '8.9505',
        'timezone': 'Europe/Berlin'
    },
    'full_cuts': 3,
    'avoid_rain': True,
    'avoid_temperature': True,
    'use_grass_growth': True,
    'no_mow_calendar_days': [
        {
            'day': 0,
            'slots': [
                {
                    'En': True,
                    'StHr': 0,
                    'StMin': 0,
                    'EnHr': 8,
                    'EnMin': 0
                },
                {
                    'En': True,
                    'StHr': 20,
                    'StMin': 0,
                    'EnHr': 23,
                    'EnMin': 59
                }
            ]
        },
        ...
        {
            'day': 6,
            'slots': [
                {
                    'En': True,
                    'StHr': 0,
                    'StMin': 0,
                    'EnHr': 23,
                    'EnMin': 59
                }
            ]
        }
    ]
}
```


## Attributes for reading data from locally cached API data
All functions that doesnt contain "update" first in name is collecting data from locally stored variables in the function. No API calls to Bosch or mower.

attributes                 | Description
-------------------------|-----------------------------
alerts_count | Show counts of the current alerts.
alerts | Show detailed list of alerts.
calendar | Get the calendar of planned mows.
AlmFirmwareVersion | Show firmware version.
AlmMode | Show mow mode.
AlmName | Show name.
BareToolNumber | Show the model number.
Battery | Show battery information.
BatteryAmbientTemp | Show the ambient temp of the battery.
BatteryCycles | Dont know what this value is?
BatteryDischarge | Show the current drawn in Ah.
BatteryPercent | Show the raw value for percentage left. For Gen 1 this seems to be the battery voltage. For Gen 2 it seems to be the actual percentage left in the battery.
BatteryPercentAdjusted | Show the adjusted value for percentage left. Calculated for Gen 1, and the actual percentage value for Gen 2.
BatteryTemp | Show temp of the battery.
BatteryVoltage | Show voltage for the battery. For Gen 1 mowers this value seems to be correct. For Gen 2 it seems to be the same value as the percentage left in battery.
ConvertBoschDateTime | Convert Bosch abbreviation for time to std 24h time
Country | Show country for the account.
Displayname | Show name for the account.
Email | Show email adress for the account.
FirmwareAvailable | Show if there are any firmware updates available.
FriendlyAlertErrorCode | Show user friendly alert error code description to be shown in HA GUI.
Garden | Dont know what this is?
HmiKeysn | Dont know what this is?
Language | Show language for the account.
MapSvgCacheTs | Dont know what this is...
MapUpdateAvailable | Show if there is an update of the map image.
ModelDescription | Show user friendly model name.
ModelVoltage | Show the predefined voltage limits in order to calculate battery percentage.
ModelVoltageMax | Show the maximum predefined voltage limits in order to calculate battery percentage.
ModelVoltageMin | Show the minimum predefined voltage limits in order to calculate battery percentage.
MowMode | Show mow mode
Mowed | Show percentage of lawn mowed
MowerState | Show current state
MowerStateDescription | Show simple description of current state. States available are Docked, Mowing, Stuck, Diagnostics mode, End of life, Software update.
MowerStateDescriptionDetailed | Show description in detail of current state.
MowingModeDescription | Show the user friendly mow mode description.
NeedsService | Show needs service flag. Dont know when it is used.
NextMow | Show next planned mow session.
OptIn | Dont know what this are for?
OptInApp | Dont know what this are for?
Runtime | Show session and total rutime and charge time in minutes.
RuntimeSession | show session runtime and charge time in minutes
RuntimeTotal | Show total runtime and charge time in hours
Serial | Show serial number
ServiceCounter | Show service counter for knives
SvgxPos | Show svg x-position of mower.
SvgyPos | Show svg y-position of mower.
XPos | Show x-position of mower.
YPos | Show y-position of mower.

## Not working

### Not properly implemented yet

    update_predicitive_calendar()
Get the calender for predicted mow sessions

    update_user_adjustment()
Get the user adjustment of the mowing frequency

    update_automatic_update()
Get the automatic update settings


# API CALLS
https://api.indego.iot.bosch-si.com:443/api/v1


```python
post
/authenticate

get
/alerts
/alms
/alms/<serial>
/alms/<serial>/automaticUpdate
/alms/<serial>/calendar
/alms/<serial>/config
/alms/<serial>/map
/alms/<serial>/network
/alms/<serial>/updates
/alms/<serial>/operatingData
/alms/<serial>/predictive
/alms/<serial>/predictive/calendar
/alms/<serial>/predictive/lastcutting
/alms/<serial>/predictive/location
/alms/<serial>/predictive/nextcutting
/alms/<serial>/predictive/schedule
/alms/<serial>/predictive/useradjustment
/alms/<serial>/predictive/weather
/alms/<serial>/security
/alms/<serial>/setup
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
