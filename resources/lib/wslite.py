
from kodi_six import xbmc, xbmcgui
import json
from resources.lib.wslsettings import loadSettings
from resources.lib.xlogger import Logger
from resources.plugins import *



class Main( xbmc.Monitor ):

    def __init__( self ):
        """Starts the background process for weather station lite."""
        xbmc.Monitor.__init__( self )
        self._init_vars()
        self.LW.log( ['background monitor version %s started' % self.SETTINGS['ADDONVERSION']], xbmc.LOGINFO )
        self.LW.log( ['debug logging set to %s' % self.SETTINGS['debug']], xbmc.LOGINFO )
        self.LW.log( ['starting external hardware interface'] )
        while not self.abortRequested():
            if self.waitForAbort( 10 ):
                break
        self.LW.log( ['background monitor version %s stopped' % self.SETTINGS['ADDONVERSION']], xbmc.LOGINFO )


    def onNotification( self, sender, method, data ):
        if 'Other.RPIWSL_VariablePass' in method:
            data = json.loads( data )
            self.LW.log( ['MONITOR METHOD: %s DATA: %s' % (str( method ), str( data ))] )
            if data == 'ScreenStatus:ScreenOff':
                self._set_property( 'ScreenStatus', 'Off' )
            else:
                self._set_properties( self.SENSORINTERFACE.getSensorData( data=data ) )
        elif 'Other.RPIWSL_SettingsRequest' in method:
            data = json.loads( data )
            self.LW.log( ['MONITOR METHOD: %s DATA: %s' % (str( method ), str( data ))] )
            self.SENSORINTERFACE.handlePassback( 'ReturningSettings', self._scrub_settings() )


    def onSettingsChanged( self ):
        self._init_vars()
        self.SENSORINTERFACE.handlePassback( 'ReturningSettings', self._scrub_settings() )


    def _init_vars( self ):
        self.WINDOWID = 12600
        self.WINDOW = xbmcgui.Window( int(self.WINDOWID) )
        self.SETTINGS = loadSettings()
        self.LW = Logger( preamble='[WS Lite Monitor]', logdebug=self.SETTINGS['debug'] )
        self.SENSORINTERFACE = self._pick_sensor_interface()


    def _pick_sensor_interface( self ):
        if self.SETTINGS['sensor_interface'] == 0:
            return rpiwsl.SensorInterface()


    def _scrub_settings( self ):
        scrubbed_settings = {}
        for thekey, thevalue in self.SETTINGS.items():
            if 'ADDON' in thekey:
                continue
            else:
                scrubbed_settings[thekey] = thevalue
        return scrubbed_settings


    def _set_properties( self, properties ):
        for oneprop in properties:
            self._set_property( oneprop[0], value=oneprop[1] )


    def _set_property( self, property_name, value='' ):
        try:
          self.WINDOW.setProperty( property_name, value )
          self.LW.log( ['%s set to %s' % (property_name, value)] )
        except Exception, e:
          self.LW.log( ['Exception: Could not set property %s to value %s' % (property_name, value), e] )
