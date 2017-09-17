#v.0.1.0
# -*- coding: utf-8 -*-

import os
from ..common.fileops import readFile


class objectConfig():
    def __init__( self ):
        pass
        
    def getSensorData( self, sensorfolder='', tempscale='°C' ):
        loglines = []
        sensordata = []
        f_loglines, alldata = readFile( os.path.join( sensorfolder, 'sensordata.txt' ) )
        loglines.extend( f_loglines )
        data_array = alldata.splitlines()
        try:
            last = data_array[-1]
        except IndexError:
            last = ''
        if last:
            all_values = last.split('\t')
            all_values.pop(0) #removes the unneeded date field from the sensor file
            for one_value in all_values:
                s_info = one_value.split(':')
                if s_info[0].endswith('Temp'):
                    sensordata.append( [s_info[0], self._convert_temp( s_info[1], tempscale )] )
                elif s_info[0].endswith('Humidity'):
                    sensordata.append( [s_info[0], s_info[1] + '%'] )
                elif s_info[0].endswith('Pressure'):
                    sensordata.append( [s_info[0], s_info[1] + 'mbar'] )
                else:
                    sensordata.append( [s_info[0], s_info[1]] )
        return sensordata, loglines	
        
    def _convert_temp( self, temperature, tempscale ):
        if tempscale == '°C':
            return temperature
        elif tempscale == '°F':
            return str( int( (float( temperature ) * 9/5) + 32 ) )
        elif tempscale == 'K':
            return str( int( float( temperature ) + 273.15 ) )
        elif tempscale == '°Ré':
            return str( int( float( temperature ) * 4/5 ) )
        elif tempscale == '°Ra':
            return str( int( (float( temperature ) * 273.15) * 9/5 ) )
        elif tempscale == '°Rø':
            return str( int( (float( temperature ) * 21/40) + 7.5 ) )
        elif tempscale == '°De':
            return str( int( (100 - float( temperature )) * 3/2 ) )
        elif tempscale == '°N':
            return str( int( (float( temperature ) * 0.33) ) )
        else:
            return temperature