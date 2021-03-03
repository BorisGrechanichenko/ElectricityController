class TemperatureSensor :
    ''' temperature sensor interface '''
  
    def __init__( self ) :
        pass

    def CurrentTemperature( path ) :
        tfile = open( path )
        text = tfile.read()
        tfile.close()
        secondLine = text.split( "\n" )[ 1 ]
        temperatureData = secondLine.split( " " )[ 9 ]
        temperature = float( temperatureData[ 2: ] )
        temperature = temperature / 1000
        return temperature
        
