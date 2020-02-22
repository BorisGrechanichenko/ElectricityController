#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import configparser
import datetime
import time

def TimerCondition( config, index ) :  # Monday is 0 in python!
    conditionCase = "condition" + str( index+1 )
    isActive = config.getint(conditionCase, "active")
    if( isActive ) :
        condDay = config.getint(conditionCase, "weekday")
        condBegin = config.getint(conditionCase, "begin_hour")
        condEnd = config.getint(conditionCase, "end_hour")
        weekDay = datetime.datetime.today().weekday()
        curHour = datetime.datetime.today().hour
        
        correctTime = ( curHour >= condBegin and curHour < condEnd )
        correctDay = ( weekDay == (condDay-1) )
        return correctTime and correctDay
    else :
        return False
    
def ActivityCondition( config ) :
    isActive = config.getint("conditions", "active")
    if( isActive ) :
        conditionsCnt = config.getint("conditions", "amount")
        for index in range(0, conditionsCnt) :
            if( TimerCondition( config, index ) ) :
                return True
        return False
    else :
        return False

def TemperatureCondition( config, temperature ) :    
    useTemperature = config.getint( "conditions", "temperature" )
    if( useTemperature ) :
        curHour = datetime.datetime.today().hour
        threshold = 1 if ( curHour < 9 and curHour > 4 ) else 1.5
        return ( temperature > threshold )

def CurrentTemperature() :
    tfile = open( "/sys/bus/w1/devices/28-0117c158edff/w1_slave" )
    text = tfile.read()
    tfile.close()
    secondLine = text.split( "\n" )[ 1 ]
    temperatureData = secondLine.split( " " )[ 9 ]
    temperature = float( temperatureData[ 2: ] )
    temperature = temperature / 1000
    return temperature

def PrepareGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def RelayOn( pin ):
    GPIO.output(pin, GPIO.LOW )

def RelayOff( pin ):
    GPIO.output( pin, GPIO.HIGH )

def PowerOn( pin ):
    RelayOff( pin )

def PowerOff( pin ):
    RelayOn( pin )
    
def InitSystem( folder ) :
    path = folder + "global_config.conf"
    print("INIT SOURCE: " + path )
    config = configparser.RawConfigParser()
    config.read( path )

    relay_section = 'relay_pins'
    pins = [ 'relay1', 'relay2', 'relay3', 'relay4', \
             'relay5', 'relay6', 'relay7', 'relay8' ]

    PrepareGPIO()
    for pin in pins:
        pin_number = config.getint(relay_section, pin)
        print("INIT PIN: "+str( pin_number ))
        GPIO.setup(pin_number, GPIO.OUT)
        RelayOff( pin_number )
    

config = configparser.RawConfigParser()
configFolder = "/home/pi/Documents/Projects/Controller/config/"
files = [ 'Water', 'OldHouse', 'NewHouse', 'Flour', 'Bathroom' ]

InitSystem(configFolder)

while True:
    temperature = CurrentTemperature()
    print( "Temperature = " + str( temperature ) )
    for file in files:
        config.read( configFolder + file + ".conf" )
        isActive = config.getint("conditions", "active")
        unpowered = False
        if( isActive == 0 ):
            print( "Inactive device " + file )
        else :
            unpowered = ActivityCondition( config )
            if( unpowered ) :
                unpowered = TemperatureCondition( config, temperature )
            print( file + " power " + ( "off" if unpowered else "on" ) )
        
        relayCnt = config.getint("relay_pins", "amount")
        for index in range(0, relayCnt) :
            pin_number = config.getint( "relay_pins", 'relay' + str( index+1 ) )
            #print( "use pin:" + str( pin_number ) )

            if( unpowered ):
                PowerOff( pin_number )
            else:
                PowerOn( pin_number )
    print( "-----" )
    time.sleep( 5 )

