import configparser
import re

class DeviceConfigParcer() :
    '''configparcer for device' config files'''
       
    def __init__( self, path ) :
        self.config = configparser.RawConfigParser()
        self.configPath = path
        self.Update()

    def GetRelays( self ) :
        relays = self.config.get( "settings", "relays" )
        return relays.split( ", " )

    def GetActivityFlag( self ) :
        try :
            return self.config.getboolean( "settings", "active", fallback = False )
        except :
            print( "Config errror: Incorrect activity flag for device!" )
            return False
            

    def GetTemperatureFlag( self ) :
        try :
            return self.config.getboolean( "settings", "temperatureControl", fallback = False )
        except :
            print( "Config errror: Incorrect temperature flag for device!" )
            return False

    def GetConditions( self ) :
        '''returns the list of tuples (pairs)'''
        result = []
        conditions = self.config.items( "conditions" )
        try :
            for line in conditions :
                if not re.match( "^(0|1),\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun){1}\s+([0-1]?[0-9]|2[0-3]):[0-5][0-9]\s+-\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun){1}\s+([0-1]?[0-9]|2[0-4]):[0-5][0-9]", line[ 1 ] ):
                    print( "Config errror: Incorrect condition for relays!" )
                    print( "Error in condition: " + line[ 1 ] )
                    return result
                s1 = line[ 1 ].split( ", " )
                if( s1[ 0 ] == "0" ) :
                    pass
                else :
                    timeLimits = s1[ 1 ].split( " - " )
                    result.append( ( timeLimits[ 0 ], timeLimits[ 1 ] ) )
        except:
            print( "Config errror: Incorrect conditions for relays!" )
            
        return result

    def Update( self ) :
        self.config.read( self.configPath )
