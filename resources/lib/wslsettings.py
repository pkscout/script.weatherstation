
from resources.lib.kodisettings import *

SETTINGSLIST = [ {'name':'auto_dim', 'default':True},
                 {'name':'fixed_brightness', 'default':100},
                 {'name':'dark_threshold', 'default':5},
                 {'name':'bright_threshold', 'default':80},
                 {'name':'dark_action', 'default':0},
                 {'name':'dim_action', 'default':4},
                 {'name':'bright_action', 'default':10},
                 {'name':'sunrise_action', 'default':11},
                 {'name':'sunrise_days', 'default':0},
                 {'name':'sunset_action', 'default':11},
                 {'name':'sunset_days', 'default':0},
                 {'name':'timed_one', 'default':'00:00'},
                 {'name':'timed_one_days', 'default':0},
                 {'name':'timed_one_action', 'default':11},
                 {'name':'timed_two', 'default':'00:00'},
                 {'name':'timed_two_days', 'default':0},
                 {'name':'timed_two_action', 'default':11},
                 {'name':'sensor_interface', 'default':0},
                 {'name':'debug', 'default':False}
               ]


def loadSettings():
    settings = {}
    settings['ADDON'] = ADDON
    settings['ADDONNAME'] = ADDONNAME
    settings['ADDONLONGNAME'] = ADDONLONGNAME
    settings['ADDONVERSION'] = ADDONVERSION
    settings['ADDONPATH'] = ADDONPATH
    settings['ADDONDATAPATH'] = ADDONDATAPATH
    settings['ADDONICON'] = ADDONICON
    settings['ADDONLANGUAGE'] = ADDONLANGUAGE
    for item in SETTINGSLIST:
        if isinstance( item['default'], bool ):
            getset = getSettingBool
        elif isinstance( item['default'], int ):
            getset = getSettingInt
        elif isinstance( item['default'], float ):
            getset = getSettingNumber
        else:
            getset = getSettingString
        settings[item['name']] = getset( item['name'], item['default'] )
    return settings




