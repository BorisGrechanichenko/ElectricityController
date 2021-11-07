currentPinStates = {}

class GPIO :
    '''fake GPIO for testing'''

    OUT = "GPIO.OUT"
    LOW = "GPIO.LOW"
    HIGH = "GPIO.HIGH"
    BCM = "GPIO.BCM"
    
    def __init__( self ) :
        print ( "---init GPIO" )

    def setup( pin_number, state ) :
        print( "---setup GPIO pin " + str( pin_number ) )

    def input( pin_number ) :
        global currentPinStates
        if pin_number in currentPinStates :
            return currentPinStates[ pin_number ]
        else :
            return 0

    def output( pin_number, state ) :
        global currentPinStates
        currentPinStates[ pin_number ] = state
        print( "---set pin " + str( pin_number ) + " to state " + str( state ) )

    def setmode( mode ) :
        print( "---setmode ", mode )

    def setwarnings( state ) :
        print( "---setwarnings ", state )
