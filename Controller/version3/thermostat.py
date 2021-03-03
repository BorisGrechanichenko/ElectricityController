import enum
import datetime
import math
from temperatureSensor import *

class ThermostatState( enum.Enum ):
    on = ( 0, "on" )
    off = ( 1, "off" )

class InternalThermostatState( enum.Enum ):
    over = 0
    fromOver = 1
    fromBelow = 2
    below = 3

class Thermostat :
    '''temperature switch with delay'''
    
    def __init__( self, path, temperature = 1 ) :
        self.referenceValue = temperature
        self.state = ThermostatState.on
        self.internalState = InternalThermostatState.over
        self.threshold = 0.5
        self.useSunHeatingCorrection = True
        self.startOfTheSunHeating = datetime.datetime.strptime( '5:00', "%H:%M")
        self.endOfTheSunHeating = datetime.datetime.strptime( '9:00', "%H:%M")
        self.sunCorrection = 0.5
        self.temperatureSensorPath = path

    def GetCurrentReferencePoint( self ) :
        '''reference temperature with the correction of morning sun heat'''
        if not self.useSunHeatingCorrection :
            return self.referenceValue
        curTime = datetime.datetime.today()
        todayStart = curTime.replace( hour = self.startOfTheSunHeating.hour, minute = self.startOfTheSunHeating.minute, second = 0, microsecond = 0 )
        todayEnd = curTime.replace( hour = self.endOfTheSunHeating.hour, minute = self.endOfTheSunHeating.minute, second = 0, microsecond = 0 )
        if ( todayStart < curTime < todayEnd ) :
            return self.referenceValue + self.sunCorrection
        else :
            return self.referenceValue
        

    def Update( self ) :
        try:
            self.currentTemperature = TemperatureSensor.CurrentTemperature( self.temperatureSensorPath )
        except FileNotFoundError:
            print( "Error: Temperature sensor wasn't found!" )
            self.state = ThermostatState.on
            return

        currentReferencePoint = self.GetCurrentReferencePoint()
        topThreshold = self.referenceValue + self.threshold
        bottomThreshold = self.referenceValue - self.threshold
        
        if self.currentTemperature >= topThreshold :
            self.state = ThermostatState.off
            self.internalState = InternalThermostatState.over
            return
        elif self.currentTemperature <= bottomThreshold :
            self.state = ThermostatState.on
            self.internalState = InternalThermostatState.below
            return

        if self.internalState == InternalThermostatState.over :
            self.internalState = InternalThermostatState.fromOver
            if self.currentTemperature <= currentReferencePoint :
                self.state = ThermostatState.on
                    
        elif self.internalState == InternalThermostatState.fromOver :
            if self.currentTemperature <= currentReferencePoint :
                self.state = ThermostatState.on
                
        elif self.internalState == InternalThermostatState.fromBelow :
            if self.currentTemperature >= currentReferencePoint :
                self.state = ThermostatState.off
                
        elif self.internalState == InternalThermostatState.below :
            self.internalState = InternalThermostatState.fromBelow
            if self.currentTemperature >= currentReferencePoint :
                self.state = ThermostatState.off
                       

    def CurrentTemperature( self ) :
        try :
            return self.currentTemperature
        except AttributeError:
            return 'unknown'
