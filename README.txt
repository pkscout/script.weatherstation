A little addon to read data from external sources and add that information to the Kodi weather window properties.

This script is designed as run and done.  The external sensor or some other script will have to trigger it to update the weather window properties.  The script has a plugin architecture so that additional sensor types can be easily added.  Plugins must support two method calls:

GetSensorInfo()
This method must return a list of dicts.  Each dict will be parsed, and a weather window property will be set with the dict reference being the property name and the dict value being the property value.  My Estuary modification uses IndoorTemp, IndoorHumidity, IndoorPressure, and AutoDim (string values of True or False).


HandlePassback( action )
The main script can accept arguments in the form of action=thing.  HandlePassback will be sent the specific action and needs to respond to it if possible.  HandlePassback returns a string telling the main script what happened (mostly just for debug logging).  My Estuary Mod currently uses the following actions:

BrightnessUp
BrightnessDown
AutoDimOn
AutoDimOff


Special Cases
The script can set an AutoDim weather window property either based on information passed back by it's plugins or by arguments sent when the script is run.  If you want the plugin to change the AutoDim status, send AutoDim with True or False in the returned list of dicts.  For script arguments:

action=AutoDimOn (sets AutoDim window property to the string True)
action=AutoDimOff (sets AutoDim window property to the string False)

