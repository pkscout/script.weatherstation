# -*- coding: utf-8 -*-

import json
from kodi_six import xbmc
from kodi_six.utils import py2_encode, py2_decode



class SensorInterface:

    def __init__( self ):
        """Initialize the sensor class."""
        self.TEMPSCALE = py2_encode( xbmc.getInfoLabel('System.TemperatureUnits') )

       
    def handlePassback( self, action ):
        message = { "jsonrpc": "2.0",
                    "method": "JSONRPC.NotifyAll",
                    "params": {"sender": "Weatherstation", "message": "RPIWSL_VariablePass", "data": {"action":action}},
                    "id": 1 }
        xbmc.executeJSONRPC( json.dumps( message ) )
        return 'passed message via websockets to rpi.weatherstation.lite'
 
 
    def getSensorData( self, data=None ):
        sensordata = []
        all_values = data.split(';')
        for one_value in all_values:
            s_info = one_value.split(':')
            if s_info[0].lower().endswith('temp'):
                sensordata.append( [s_info[0], self._convert_temp( s_info[1] )] )
            elif s_info[0].lower().endswith('humidity'):
                sensordata.append( [s_info[0], self._convert_humidity( s_info[1] )] )
            elif s_info[0].lower().endswith('pressure'):
                sensordata.append( [s_info[0], self._convert_pressure( s_info[1] )] )
            else:
                sensordata.append( [s_info[0], s_info[1]] )
        return sensordata

        
    def _convert_humidity( self, humidity ):
        if humidity.lower() == 'none':
            return ''
        return str( int( round( float( humidity ) ) ) ) + '%'


    def _convert_pressure( self, pressure ):
        if pressure.lower() == 'none':
            return ''
        if self.TEMPSCALE == '°F':
            return '%.2f' % (float( pressure ) * 0.0295301) + ' inHg'
        else:
            return pressure + ' mbar'
    
    
    def _convert_temp( self, temperature ):
        if temperature.lower() == 'none':
            return ''
        if self.TEMPSCALE == py2_encode( '°C' ):
            temp_float =  float( temperature )
        elif self.TEMPSCALE == py2_encode( '°F' ):
            temp_float = (float( temperature ) * 9/5) + 32
        elif self.TEMPSCALE == py2_encode( 'K' ):
            temp_float = float( temperature ) + 273.15
        elif self.TEMPSCALE == py2_encode( '°Ré' ):
            temp_float = float( temperature ) * 4/5
        elif self.TEMPSCALE == py2_encode( '°Ra' ):
            temp_float = float( temperature ) * 273.15 * 9/5
        elif self.TEMPSCALE == py2_encode( '°Rø' ):
            temp_float = (float( temperature ) * 21/40) + 7.5
        elif self.TEMPSCALE == py2_encode( '°De' ):
            temp_float = (100 - float( temperature )) * 3/2
        elif self.TEMPSCALE == py2_encode( '°N' ):
            temp_float = float( temperature ) * 0.33
        else:
            temp_float =  float( temperature )
        return str( int( round( temp_float ) ) )

