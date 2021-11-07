import enum
import re
import datetime
from relayBoard import *
from thermostat import *
from deviceConfigParcer import *
from logger import *

class Device :
    ''' device connected via GPIO relay board '''

    weekdays = { 'Mon' : 0, 'Tue' : 1, 'Wed' : 2, 'Thu' : 3, 'Fri' : 4, 'Sat' : 5, 'Sun' : 6 }
    useTemperatureSensor = True

    def __init__( self, relayBoard, configPath ) :
        self.title = re.split( '\.|config/|config\\|\\|/', configPath )[-2]
        self.parcer = DeviceConfigParcer( configPath )
        self.active = self.parcer.GetActivityFlag()
        self.unpowered = False
        self.temperatureControl = False
        self.switchedOnByLowTemperature = False
        self.relays = []
        for relayName in self.parcer.GetRelays() :
            self.relays.append( relayBoard.Relay( relayName ) )

    def SetThermostat( self, tst ) :
        self.thermostat = tst

    def SetLogger( self, log ) :
        self.logger = log

    def Update( self ) :
        self.UpdateParcerData()

        if not self.active :
            if self.unpowered :
                self.logger.write( self.title + " switched on." )
                self.SwitchPowerOn()
            self.switchedOnByLowTemperature = False
            return

        if self.TemporaryActivityCondition( self.parcer.GetTemporaryActivityConditions() ) :
            if self.unpowered :
                self.logger.write( self.title + " switched on by the temporary condition." )
                self.SwitchPowerOn()
            self.switchedOnByLowTemperature = False
            return
        
        if( self.temperatureControl ) :
            if( self.thermostat.state == ThermostatState.on ) :
                if self.unpowered :
                    self.logger.write( self.title + " switched on. Temperature = " + str( self.thermostat.CurrentTemperature() ) )
                    self.switchedOnByLowTemperature = True
                    self.SwitchPowerOn()
                return

        shutdownTime = self.TimerCondition( self.parcer.GetConditions() )
        if shutdownTime and not self.unpowered :
            self.logger.write( self.title + " switched off." + ( " Temperature = " + str( self.thermostat.CurrentTemperature() ) if self.switchedOnByLowTemperature else "" ) )
            self.SwitchPowerOff()
        elif not shutdownTime and self.unpowered :
            self.logger.write( self.title + " switched on." )
            self.SwitchPowerOn()

        self.switchedOnByLowTemperature = False


    def UpdateParcerData( self ) :
        self.parcer.Update()
        active = self.parcer.GetActivityFlag()
        if( self.active != active ) :
            self.logger.write( "Device \"" + self.title + ( "\" des" if not active else "\" " ) + "activated" )
            if active and self.useTemperatureSensor :
                self.logger.write( "Temperature control for \"" + self.title + "\" is " + ( " in" if not self.temperatureControl else "" ) + "active" )
        self.active = active

        if self.useTemperatureSensor :
            temperatureControl = self.parcer.GetTemperatureFlag()
            if( self.active and self.temperatureControl != temperatureControl ) :
                self.logger.write( "Temperature control for \"" + self.title + "\" was " + ( " des" if not temperatureControl else "" ) + "activated" )
            self.temperatureControl = temperatureControl

    def TemporaryActivityCondition( self, conditions ) :
##        print( conditions )
        for condition in conditions :
            if condition[ 0 ] <= datetime.datetime.today() <= condition[ 1 ] :
                return True
        return False

    def TimerCondition( self, conditions ) :
        '''timer condition for the device to be switched off'''
        for condition in conditions :
            start = self.FindDate( datetime.datetime.today(), condition[ 0 ], True )
            end = self.FindDate( start, condition[ 1 ], False )
            if '24:00' in condition[ 1 ] : #костыль2! :(
                end += datetime.timedelta( minutes = 1 )
##            print( start, end, datetime.datetime.today(), condition )
            if( start <= datetime.datetime.today() <= end ):
                return True
        return False

    def FindDate( self, referenceDate, timeLimit, searchInThePast ) :
        limit = timeLimit.split()
        weekday = self.weekdays[ limit[ 0 ] ]            
        limitTime = self.DateTimeFromHoursAndMinutesStrings( limit[ 1 ] )
        result = referenceDate.replace( hour = limitTime.hour, minute = limitTime.minute, second = 0, microsecond = 0 )
        refWeekDay = referenceDate.weekday()
        dif = abs( refWeekDay - weekday )
        if refWeekDay == weekday :
            return result
        if( searchInThePast ) :
            if refWeekDay > weekday :            
                return result - datetime.timedelta( days = dif )
            else :
                return result - datetime.timedelta( days = 7 - weekday + refWeekDay )
        else:
            if refWeekDay < weekday:            
                return result + datetime.timedelta( days = dif )
            else :
                return result + datetime.timedelta( days = 7 - refWeekDay + weekday )

    def DateTimeFromHoursAndMinutesStrings ( self, string ) :
        tstr = string.replace( '24:00', '23:59' ) #костыль1! :(
        return datetime.datetime.strptime( tstr, "%H:%M")

    def SwitchPowerOn( self ) :
        self.unpowered = False
        for relay in self.relays :
            relay.PowerOn()
    
    def SwitchPowerOff( self ) :
        self.unpowered = True
        for relay in self.relays :
            relay.PowerOff()
