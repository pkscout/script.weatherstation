# *  Credits:
# *
# *  original Weather Station Code by pkscout

import os, sys, xbmc, xbmcaddon, xbmcgui, xbmcvfs
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
    plugin = imp_plugin.objectConfig( addon=addon )
    active, priority = _get_plugin_settings( module )
    if active == 'true':
        plugins['objs'][module] = plugin
        plugins['names'].append( [priority, module] )
        lw.log( ['added %s to weather sensor plugins' % module] )



class Main:

    def __init__( self ):
        self.WINDOWID = 12600
        self.WINDOW = xbmcgui.Window( int(self.WINDOWID) )
   

    def GetSensorInfo( self ):
        sensordata = []
        try:
            plugins['names'].sort( key=lambda x: x[0] )
        except TypeError:
            pass
        for plugin_name in plugins['names']:
            lw.log( ['checking %s for sensor data' % plugin_name[1]] )
            sensordata = plugins['objs'][plugin_name[1]].getSensorData()
            if sensordata:
                lw.log( ['got sensor data from %s, so stop looking' % plugin_name[1]] )
                break
        self._set_properties( sensordata )


    def HideCursor( self ):
        self._replace_pointer_xml( 'Pointer-Hidden.xml' )
        
    
    def ShowCursor( self ):
        self._replace_pointer_xml( 'Pointer-Visible.xml' )


    def Passback( self, action ):
        try:
            plugins['names'].sort( key=lambda x: x[0] )
        except TypeError:
            pass
        for plugin_name in plugins['names']:
            data = ''
            if action == 'AutoDimOn':
                self._set_property( 'AutoDim', 'True' )
            elif action == 'AutoDimOff':
                self._set_property( 'AutoDim', 'False' )
            elif action == 'ScreenOff':
                self._set_property( 'ScreenStatus', 'Off' )
            elif action == 'ScreenOn':
                self._set_property( 'ScreenStatus', 'On' )
            lw.log( ['passing action %s to %s' % (action, plugin_name[1])] )
            result = plugins['objs'][plugin_name[1]].handlePassback( action )
            lw.log( ['got %s back from %s' % (result, plugin_name[1])] )


    def _replace_pointer_xml( self, newfile ):
        addon_dir_path = os.path.join( addonpath, '..' )
        skin_xml_path = os.path.join( addon_dir_path, xbmc.getSkinDir(), 'xml' )
        current_xml = os.path.join( skin_xml_path, 'Pointer.xml' )
        replacement_xml = os.path.join( skin_xml_path, newfile )
        lw.log( ['copying %s to %s' % (replacement_xml, current_xml)] )
        xbmcvfs.copy( replacement_xml, current_xml )


    def _set_properties( self, properties ):
        for property in properties:
            self._set_property( property[0], property[1] )
        

    def _set_property( self, property_name, value=""):
        #sets a property (or clears it if no value is supplied)
        #does not crash if e.g. the window no longer exists.
        try:
          self.WINDOW.setProperty( property_name, value )
          lw.log( ['%s set to %s' % (property_name, value)] )
        except Exception, e:
          lw.log( ["Exception: Couldn't set propery " + property_name + " value " + value , e])


def _parse_argv():
    try:
        params = dict( arg.split( "=" ) for arg in sys.argv[ 1 ].split( "&" ) )
    except IndexError:
        params = {}        
    except Exception, e:
        lw.log( ['unexpected error while parsing arguments', e] )
        params = {}
    return params.get( "action", "GetSensorInfo")


if ( __name__ == "__main__" ):
    lw.log( ['script version %s started' % addonversion], xbmc.LOGNOTICE )
    lw.log( ['debug logging set to %s' % logdebug], xbmc.LOGNOTICE )
    ws = Main()
    action = _parse_argv()
    if action == 'GetSensorInfo':
        ws.GetSensorInfo()
    elif action == 'HideCursor':
        ws.HideCursor()
    elif action == 'ShowCursor':
        ws.ShowCursor()
    else:
        ws.Passback( action )
lw.log( ['script stopped'], xbmc.LOGNOTICE )
