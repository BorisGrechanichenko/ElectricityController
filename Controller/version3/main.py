import time
import sys
from os import listdir
from device import *

config = configparser.RawConfigParser()
config.read( 'config/global_config.conf' )
logger = Logger( config.get( "settings", "logFileName" ) )
try :
    logger.writeLog = config.get( "settings", "writeLog" )
except :
    print( "Incorrect config flag for writing log file. Logging is on." )
logger.write( "---------- Electricity controller started ----------" )
useTemperatureSensor = False
try :
    useTemperatureSensor = config.getboolean( "settings", "useTemperatureSensor" )
except :
    logger.write( "Incorrect config flag for using temperature sensor. Temperature control is switches off." )

relayBoard = RelayBoard()
relayBoard.SelLogger( logger )
try :
    relayBoard.InitBoard( 'config/global_config.conf' )
except Exception as ex:
    logger.write( "Error occured on initialisation of the relays from config file" )
    logger.write( "Error: %s" % ex )
    exit()

thermostat = Thermostat( path = config.get( "thermostatSettings", "temperatureSensorPath" ) )
if useTemperatureSensor :
    try :
        thermostat.referenceValue = config.getfloat( "thermostatSettings", "lowTemperatureValue" )
        thermostat.threshold = config.getfloat( "thermostatSettings", "temperatureThreshold" )
        thermostat.useSunHeatingCorrection = config.getboolean( "thermostatSettings", "useSunHeatingCorrection" )
        thermostat.startOfTheSunHeating = datetime.datetime.strptime( config.get( "thermostatSettings", "startOfTheSunHeating" ), "%H:%M") 
        thermostat.endOfTheSunHeating = datetime.datetime.strptime( config.get( "thermostatSettings", "endOfTheSunHeating" ), "%H:%M") 
        thermostat.sunCorrection = config.getfloat( "thermostatSettings", "sunCorrection" )
        logger.write( "Temperature control starts from " + str( thermostat.referenceValue ) + \
                      " degrees with threshold = " + str( thermostat.threshold ) + " degrees. " + \
                      "Sun adjustment is switched " + "on." if thermostat.useSunHeatingCorrection else "off." )
        if thermostat.useSunHeatingCorrection :
            logger.write( "Sun adjustment period: " + thermostat.startOfTheSunHeating.strftime( "%H:%M" ) + \
                          " - " + thermostat.endOfTheSunHeating.strftime( "%H:%M" ) +
                          ". Adjustment value = " + str( thermostat.sunCorrection ) + " degrees." )
    except Exception as ex:
        logger.write( "Error occured on initialisation of the thermostat' settings. Using default settings" )
        logger.write( "Error: %s" % ex )

devices = []
deviceFilesList = listdir( 'config' )
deviceFilesList.remove( 'global_config.conf' )
for filename in deviceFilesList :
    try :
        device = Device( relayBoard, 'config/' + filename )
        device.useTemperatureSensor = useTemperatureSensor
        device.SetLogger( logger )
        devices.append( device )
        relaysForTheDevice = '&'.join( relay.title for relay in device.relays )
        logger.write( "Device \"" + device.title + "\" (" + relaysForTheDevice + ") is " + ( "in" if not device.active else "" ) + "active" )
    except Exception as ex:
        logger.write( "Can't create device from file\"" + filename + "\"" )
        logger.write( "Error: %s" % ex )

for device in devices :
    device.SetThermostat( thermostat )
    device.Update()

updatePeriod = 5
try :
    updatePeriod = config.getint( "settings", "updatePeriod" )
    logger.write( "Using update period = " + str( updatePeriod ) + " seconds" )
except Exception as ex:
    print( "Incorrect value for the updates periods. Using default value 5 seconds" )
    logger.write( "Error: %s" % ex )
    
while True:
    if useTemperatureSensor :
        thermostat.Update()
    for device in devices :
        device.Update()
        if( device.active ) :
            print( device.title + " - power " + ( "off" if device.unpowered else "on" ) )
        else :
            print( device.title + " is inactive" )
    print( "-----" )
    time.sleep( updatePeriod )
