# Changelog

## 2.0.1
- Removing AIOFile from the package to get the pypi packgare to load

## 2.0.0
- Fix problems with pypi pakcgae not loading

## 2.0.0b2
- Tryong out new code

## 2.0.0b1
- Totally rewritten all code (thanks to Eduard!)

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
