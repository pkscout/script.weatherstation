# *  Credits:
# *
# *  original Artist Slideshow code by ronie
# *  updates and additions since v1.3.0 by pkscout
# *
# *  divingmule for script.image.lastfm.slideshow
# *  grajen3 for script.ImageCacher
# *  sfaxman for smartUnicode
# *
# *  code from all scripts/examples are used in script.artistslideshow
# *  
# *  Last.fm:      http://www.last.fm/
# *  fanart.tv:    http://www.fanart.tv
# *  theaudiodb:   http://www.theaudiodb.com
# *  htbackdrops:  http://www.htbackdrops.org

import xbmc, xbmcaddon, xbmcgui, xbmcvfs
import itertools, os, random, re, sys, time
from resources.common.xlogger import Logger
import resources.plugins

addon        = xbmcaddon.Addon()
addonname    = addon.getAddonInfo('id')
addonversion = addon.getAddonInfo('version')
addonpath    = addon.getAddonInfo('path').decode('utf-8')
addonicon    = xbmc.translatePath('%s/icon.png' % addonpath )
language     = addon.getLocalizedString
preamble     = '[Weather Station]'
logdebug     = addon.getSetting( "logging" ) 

lw = Logger( preamble=preamble, logdebug=logdebug )

# this section imports all the weather sensor plugins and initializes them
def _get_plugin_settings( module ):
    try:
        active = addon.getSetting( module )
    except ValueError:
        active = 'false'
    except Exception, e:
        lw.log( ['unexpected error while parsing weather sensor active setting for %s' % module, e] )
        active = 'false'        
    if active == 'true':
        try:
            priority = int( addon.getSetting( "priority_" + module ) )
            lw.log( ['set priority for %s to %s' % (module, priority)] )
        except ValueError:
            priority = 10
        except Exception, e:
            lw.log( ['unexpected error while parsing priority for %s' % module, e] )
            priority = 10
    else:
        priority = 10
    return active, priority

plugins = {'names':[], 'objs':{}}
for module in resources.plugins.__all__:
    full_plugin = 'resources.plugins.' + module
    __import__( full_plugin )
    imp_plugin = sys.modules[ full_plugin ]
    lw.log( ['loaded plugin ' + module] )
    plugin = imp_plugin.objectConfig()
    active, priority = _get_plugin_settings( module )
    if active == 'true':
        plugins['objs'][module] = plugin
        plugins['names'].append( [priority, module] )
        lw.log( ['added %s to weather sensor plugins' % module] )


class Main:

    def __init__( self ):
        self._get_settings()
        self._init_vars()
        while (self._on_weather_window() and not xbmc.abortRequested):
            self._set_properties( self._get_sensorinfo() )
            self._wait( self.WAITTIME )
   

    def _get_sensorinfo( self ):
        sensordata = []
        try:
            plugins['names'].sort( key=lambda x: x[0] )
        except TypeError:
            pass
        for plugin_name in plugins['names']:
            lw.log( ['checking %s for sensor data' % plugin_name[1]] )
            s_foldername = addon.getSetting( 'folder_' + plugin_name[1] )
            t_scale = xbmc.getInfoLabel('System.TemperatureUnits')
            sensordata, loglines = plugins['objs'][plugin_name[1]].getSensorData( sensorfolder=s_foldername, tempscale=t_scale )
            lw.log( loglines )
            if sensordata:
                lw.log( ['got sensor data from %s, so stop looking' % plugin_name[1]] )
                lw.log( sensordata )
                break
        if sensordata:
            return sensordata
        else:
            return []


    def _get_settings( self ):
        self.WAITTIME = int( addon.getSetting( 'waittime' ) ) * 60


    def _init_vars( self ):
        self.WINDOWID = 12600
        self.WINDOW = xbmcgui.Window( int(self.WINDOWID) )
        

    def _on_weather_window( self ):
        if xbmcgui.getCurrentWindowId() == self.WINDOWID:
            return True
        else:
            return False
    

    def _set_properties( self, sensordata ):
        for one_entry in sensordata:
            self._set_property( one_entry[0], one_entry[1] )
        

    def _set_property( self, property_name, value=""):
        #sets a property (or clears it if no value is supplied)
        #does not crash if e.g. the window no longer exists.
        try:
          self.WINDOW.setProperty( property_name, value )
          lw.log( ['%s set to %s' % (property_name, value)] )
        except Exception, e:
          lw.log( ["Exception: Couldn't set propery " + property_name + " value " + value , e])


    def _wait( self, wait_time ):
        lw.log( ['waiting %s minutes to read from sensor again' % addon.getSetting( 'waittime' )] )
        waited = 0
        while( waited < wait_time ):
            time.sleep(0.1)
            waited = waited + 0.1
            if xbmc.abortRequested or not self._on_weather_window():
                return


if ( __name__ == "__main__" ):
    lw.log( ['script version %s started' % addonversion], xbmc.LOGNOTICE )
    lw.log( ['debug logging set to %s' % logdebug], xbmc.LOGNOTICE )
    weatherstation = Main()
lw.log( ['script stopped'], xbmc.LOGNOTICE )
