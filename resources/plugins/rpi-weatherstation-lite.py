#v.0.2.0
# -*- coding: utf-8 -*-

import os, sys, xbmc
from ..common.xlogger import Logger
if sys.version_info >= (2, 7):
    import json as _json
else:
    import simplejson as _json



class objectConfig():
    def __init__( self, addon ):
        self.LW = Logger( preamble='[WS Lite - SenseHAT]', logdebug=addon.getSetting( "logging" ) )
        self.TEMPSCALE = xbmc.getInfoLabel('System.TemperatureUnits')

       
    def handlePassback( self, action ):
        message = { "jsonrpc": "2.0",
                    "method": "JSONRPC.NotifyAll",
                    "params": {"sender": "Weatherstation", "message": "RPIWSL_VariablePass", "data": {"action":action}},
                    "id": 1 }
        xbmc.executeJSONRPC( _json.dumps( message ) )
        return 'passed message via websockets to rpi.weatherstation.lite'
 
    def getSensorData( self, data=None ):
        sensordata = []
        all_values = data.split(';')
        for one_value in all_values:
            s_info = one_value.split(':')
            if s_info[0].endswith('Temp'):
                if s_info[1] is not 'None':
                    sensordata.append( [s_info[0], self._convert_temp( s_info[1] )] )
            elif s_info[0].endswith('Humidity'):
                if s_info[1] == 'None':
                    humidity = ''
                else:
                    humidity = s_info[1] + '%'
                sensordata.append( [s_info[0], humidity] )
            elif s_info[0].endswith('Pressure'):
                sensordata.append( [s_info[0], self._convert_pressure( s_info[1] )] )
            else:
                sensordata.append( [s_info[0], s_info[1]] )
        self.LW.log( ['returning sensor data', sensordata] )
        return sensordata

        
    def _convert_pressure( self, pressure ):
        if pressure == 'None':
            return ''
        if self.TEMPSCALE == '°F':
            return '%.2f' % (float( pressure ) * 0.0295301) + ' inHg'
        else:
            return pressure + ' mbar'
    
    
    def _convert_temp( self, temperature ):
        if temperature == 'None':
            return ''
        if self.TEMPSCALE == '°C':
            temp_float =  float( temperature )
        elif self.TEMPSCALE == '°F':
            temp_float = (float( temperature ) * 9/5) + 32
        elif self.TEMPSCALE == 'K':
            temp_float = float( temperature ) + 273.15
        elif self.TEMPSCALE == '°Ré':
            temp_float = float( temperature ) * 4/5
        elif self.TEMPSCALE == '°Ra':
            temp_float = float( temperature ) * 273.15 * 9/5
        elif self.TEMPSCALE == '°Rø':
            temp_float = (float( temperature ) * 21/40) + 7.5
        elif self.TEMPSCALE == '°De':
            temp_float = (100 - float( temperature )) * 3/2
        elif self.TEMPSCALE == '°N':
            temp_float = float( temperature ) * 0.33
        else:
            temp_float =  float( temperature )
        return str( int( round( temp_float ) ) )

