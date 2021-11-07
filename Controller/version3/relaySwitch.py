try:
    import RPi.GPIO as GPIO
except ImportError:
    '''fake GPIO for desktop'''
    print( "Using fake GPIO!" )
    from GPIO import *

class Relay :

    '''relay unit connected via GPIO'''

    def __init__( self, pin_number, title ) :
        self.pin = pin_number
        self.title = title
        GPIO.setup( pin_number, GPIO.OUT )

    def State( self ) :
        return GPIO.input( self.pin )
    
    def RelayOn( self ) :
        GPIO.output( self.pin, GPIO.LOW )

    def RelayOff( self ) :
        GPIO.output( self.pin, GPIO.HIGH )

    def PowerOn( self ) :
        GPIO.output( self.pin, GPIO.HIGH )

    def PowerOff( self ) :
        GPIO.output( self.pin, GPIO.LOW )
