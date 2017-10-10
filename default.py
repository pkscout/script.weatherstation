# *  Credits:
# *
# *  original Weather Station Lite Code by pkscout

import os, sys, xbmc, xbmcaddon, xbmcgui, xbmcvfs
from resources.common.xlogger import Logger
import resources.plugins

addon        = xbmcaddon.Addon()
addonname    = addon.getAddonInfo('id')
addonversion = addon.getAddonInfo('version')
addonpath    = addon.getAddonInfo('path').decode('utf-8')
addonicon    = xbmc.translatePath('%s/icon.png' % addonpath )
language     = addon.getLocalizedString
preamble     = '[WS Lite]'
logdebug     = addon.getSetting( "logging" ) 

lw = Logger( preamble=preamble, logdebug=logdebug )

# this section imports all the weather sensor plugins and initializes them
plugins = {'names':[], 'objs':{}}
for module in resources.plugins.__all__:
    full_plugin = 'resources.plugins.' + module
    __import__( full_plugin )
    imp_plugin = sys.modules[ full_plugin ]
    lw.log( ['loaded plugin ' + module] )
    plugin = imp_plugin.objectConfig( addon=addon )
    plugins['objs'][module] = plugin
    plugins['names'].append( [1, module] )
    lw.log( ['added %s to weather sensor plugins' % module] )



class Main:

    def __init__( self ):
        self.WINDOWID = 12600
        self.WINDOW = xbmcgui.Window( int(self.WINDOWID) )
   

    def GetSensorInfo( self, target=None, data=None ):
        try:
            sensordata = plugins['objs'][target].getSensorData( data = data )
        except KeyError:
            lw.log( ['no plugin found with the name ' + target] )
            sensordata = []
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
    params = {}
    for arg in sys.argv:
        arg_parts = arg.split( '=' )
        try:
            params[arg_parts[0]] = arg_parts[1]
        except IndexError:
            pass
    return params.get( 'action', None), params.get( 'plugin', None), params.get( 'data', None)


if ( __name__ == "__main__" ):
    lw.log( ['script version %s started' % addonversion] )
    lw.log( ['debug logging set to %s' % logdebug] )
    ws = Main()
    action, target, data = _parse_argv()
    if action is not None:
        if action.lower() == 'updatekodi':
            ws.GetSensorInfo( target = target, data = data )
        elif action.lower() == 'hidecursor':
            ws.HideCursor()
        elif action.lower() == 'showcursor':
            ws.ShowCursor()
        else:
            ws.Passback( action )
lw.log( ['script stopped'] )
