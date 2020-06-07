# *  Credits:
# *
# *  original Weather Station Lite Code by pkscout

from kodi_six import xbmcgui
import sys
from resources.lib.wslsettings import loadSettings
from resources.lib.xlogger import Logger
from resources.plugins import *

SETTINGS = loadSettings()
LW = Logger( preamble='[WS Lite]', logdebug=SETTINGS['debug'] )



class Main:

    def __init__( self ):
        LW.log( ['script version %s started' % SETTINGS['ADDONVERSION']] )
        LW.log( ['debug logging set to %s' % SETTINGS['debug']] )
        self._init_vars()
        action, data = self._parse_argv()
        if action:
            if action.lower() == 'updatekodi':
                self._set_properties( self.SENSORINTERFACE.getSensorData( data=data ) )
            else:
                self._passback( action )
        LW.log( ['script stopped'] )


    def _passback( self, action ):
        if action == 'AutoDimOn':
            self._set_property( 'AutoDim', 'True' )
        elif action == 'AutoDimOff':
            self._set_property( 'AutoDim', 'False' )
        elif action == 'ScreenOff':
            self._set_property( 'ScreenStatus', 'Off' )
        elif action == 'ScreenOn':
            self._set_property( 'ScreenStatus', 'On' )
        LW.log( ['passing action %s' % action] )
        result = self.SENSORINTERFACE.handlePassback( action )
        LW.log( ['got back: %s' % result] )


    def _init_vars( self ):
        self.WINDOWID = 12600
        self.WINDOW = xbmcgui.Window( int(self.WINDOWID) )
        self.SENSORINTERFACE = self._pick_sensor_interface()


    def _parse_argv( self ):
        params = {}
        for arg in sys.argv:
            arg_parts = arg.split( '=' )
            try:
                params[arg_parts[0]] = arg_parts[1]
            except IndexError:
                pass
        return params.get( 'action', None), params.get( 'data', None)


    def _pick_sensor_interface( self ):
        if SETTINGS['sensor_interface'] == 0:
            return rpiwsl.SensorInterface()


    def _set_properties( self, properties ):
        for oneprop in properties:
            self._set_property( oneprop[0], oneprop[1] )


    def _set_property( self, property_name, value=""):
        try:
          self.WINDOW.setProperty( property_name, value )
          LW.log( ['%s set to %s' % (property_name, value)] )
        except Exception, e:
          LW.log( ["Exception: Couldn't set propery " + property_name + " value " + value , e] )
