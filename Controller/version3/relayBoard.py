#import RPi.GPIO as GPIO
from relaySwitch import *
import configparser

class RelayBoard :

    '''relays board connected via GPIO'''
    CONFIG_PATH = 'config\global_config.conf'
    relays = {}

    def __init__( self ) :
        self.PrepareGPIO()

    def InitBoard( self, path = CONFIG_PATH ) :
        '''init relays defined in configuration file'''
        config = configparser.RawConfigParser()
        config.read( path )
        relaysItems = config.items( 'relay_pins' );
        self.InitRelays( relaysItems )

    def SelLogger( self, log ) :
        self.logger = log
        
    def InitRelays( self, relaysItems ) :
        '''init relays from the list of tuples (name,pin)'''
        for item in relaysItems:
            relay = Relay( int( item[ 1 ] ), item[ 0 ] )
            self.relays[ item[ 0 ] ] = relay
            self.logger.write( "INIT PIN " + str( relay.pin ) + " as " + item[ 0 ] )
            relay.PowerOn()

    def PrepareGPIO( self ) :
        GPIO.setmode( GPIO.BCM )
        GPIO.setwarnings( False )

    def Relay( self, name ) :
        return self.relays[ name ]
        
