# Changelog

## 2.0.20
- Added Calendar class and update_calendar methods
- Added delete_alert
- Added patch_alert_read -> untested!
- Moved state_description and state_description_detail to properties
- Reorders everything alphabetically, in Base kept the _ and regular update methods together and moved other internal methods down
- Redid some relogging logic, noticed a 401 after logging in also tried to relogin, even though that means login didn't work and the creds are wrong.
- Made serial optional parameter, and changed login to get serial from the endpoint in that case.
- Added serial property
- Added check for max longpoll time
- Cleaned and improved Readme

## 2.0.19
- Faulty tag/troubleshooting

## 2.0.18
- Faulty tag/troubleshooting

## 2.0.17
- Added the update_security call
- Added the update_setup call
- Added support for longpoll to get state from API
- Updates to doc

## 2.0.16
- Added the update_config call
- Added the update_network call
- Updates to doc

## 2.0.15
- Changes to state with longpoll
- Updates to poll if apdate is available
- Cleanup
- Updates to doc

## 2.0.13
- Tested and made some fixes for Longpoll functionality
- Docs updated

## 2.0.12
- Changed login logic
- Added logging for log in in and other responses

## 2.0.11
- Changed time representation for BochTime
- Docstrings added
- Some updates to README

## 2.0.10
- Changed time representation for BochTime
- Do not handle login fail in pyIndego

## 2.0.9
- Added init of alerts_count
- More error messages in log when login get request fails

## 2.0.8
- Added some logging
- More error messages in log when get request fails

## 2.0.7
- Fixed Alerts_count for alert sensor

## 2.0.6
- Adjusted time conversino for BoshTime to Swedish time format

## 2.0.5
- Adjusted session cut to convert None to 0

## 2.0.4
- Adjusted State Sensor Detail async code

## 2.0.3
- Adjusted State Sensor Detail code

## 2.0.2
- Adjusted State Sensor code

## 2.0.1
- Removing AIOFile from the package to get the pypi packgare to load

## 2.0.0
- Fix problems with pypi pakcgae not loading

## 2.0.0b2
- Tryong out new code

## 2.0.0b1
- Totally rewritten all code (thanks to Eduard!)
=======
## 1.0.21
- Spelling errors fixed
- Removed some uneccesary log messages

## 1.0.20
- Added mower state for offline

## 1.0.19
- Corrected error in database

## 1.0.18
- Added version control with new branch in github

## 1.0.17
- Added a bunch of state descriptions

## 1.0.16
- Better detection of offline mower

## 1.0.15
- Corrected state 260 as Charging (was Docked)


## 1.0.14
- Corrected error in login call

## 1.0.13
- Better handling of server responding with no content.
- Better information in log messages.
- Added getMap for downloading map image in SVN format.

## 1.0.12
- Added control for the getLongpollState to make sure that getState has been called.
- Added better handling and logging when mower is offline.
- Cleaned up some logging.

## 1.0.11
- Added support for the Indego m+ 700 mower.
- Updated get code in order to be able to login if sessin cookie is not accepted

## 1.0.10
- Added getNetwork, collects data on the mobile network the Indego is connected to.
- Added errorhandling for getState

## 1.0.9
- Added mower "Indego 400+ 2020" to database
- Divided logging of python module to different levels. Info, warning, error.

## 1.0.8
- Added getForcedState: force the API-server to get a complete update of the status. Can be used to  obtain a new position every 5-6 seconds and to replicate the moving mower on a map (like the official  app).
- Added getLongpollState. This can be used to make a call to the API aserver and then wait for a change in state instead of polling often to catch a state. Reduces traffic to/from the API server.
- Changes in get-function. Get now takes 3 arguments: self, method, timeout. This makes it more simple if the get requires longer timeout settings in any future calls.
- Renamed xPos() and yPos() to XPos() and YPos()

## 1.0.7
- Added logging if error occurs when fetching Battery max/min from database.

## 1.0.6
- Misconfiguration in mower database.

## 1.0.5
- Added better handling for unknowm mower models. Warning messages are raised in log file with model number.

## 1.0.4
- Corrected misspelling on getLastCompletedMow and related functions

## 1.0.3
- Renamed getLastCutting to getLastCompletedMow
- Renamed getNextCutting to getNextMow

## 1.0.2
- Fixed a bug in Alert handling

## 1.0.1
- Removed some extensive logging
- Rewrote the putCommand and putMowMode for more simple coding

## 1.0.0
- Added putMowMode for activating/deactivating Smart Mow.
- Corrected getLastCutting and getNextCutting, now properly implemented.

## 0.8.12
- Added getLocation for getting the Long and Lat to the garden/mower.

## 0.8.11 2020-06-06
- Adjusted call for Net Mow to handle when Smart Mow and Calendar are shut off to Manual mow mode.

## 0.8.0 2020-05-25
- Removed CI Azure Pipeline
- Code refacturing for more stable API key cache (stil not 100%)
- Work with logging for debugging

## 0.7.11 2019-08-27

### Changes
- Added support for last completed lawn mowe
- Added support for CI with Azure pipelines (for testing code before releases)

## 0.7.8 2019-08-22

### Changes
- Updated Readme

## 0.7.7 2019-08-22

### Changes
- Handle API timeout without error
- Added the netpredictive cutting API call, seems to get the last command sent to the mower

## 0.7.6 2019-08-21

### Changes
- AlertDescription: Added ID as property.

## 0.7.5 2019-08-20

### Changes
- FriendlyAlertErrorCode: Added function to get Friendly Description and handle codes that are not known.

## 0.7.4 2019-08-14

### Changes
- getAlerts: Added Friendly Description as attribute.

## 0.7.3 2019-08-14

### Changes
- getAlerts: Convert Alert name (datetime) from 2019-08-13T13:45:39.990Z to 2019-08-13 13:45.

## 0.7.2 2019-08-14

### Changes
- Finetuning functions for clearing Alerts in Alerts list

## 0.7.1 2019-08-13

### Changes
- Adjusted files to GitHub
- Updated documentation
- Perparing for reading Alerts as a list

## 0.7.0 2019-08-12

### Changes
- Added functions for max and min percentage.
- Added Percentage Adjusted to calculate percentage for Indego Gen 1 mowers.
- Bumped version number to correlate to component version
