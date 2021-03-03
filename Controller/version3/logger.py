import datetime

class Logger :
    ''''''

    def __init__( self, path = 'log.txt' ) :
        self.f = open( path, 'a' )
        self.writeLog = True

    def write( self, msg ) :
        if self.writeLog :
            self.f.write( self.decorateMessage( msg ) )
            self.f.flush()
        print( msg )

    def decorateMessage( self, msg ) :
        dt = datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S ")
        return dt + msg + '\n'
        
    def __del__( self ) :
        self.f.close()
