#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import configparser
import datetime
import time

def TimerCondition( config ) : # Monday is 0 in python!
    condDay = config.getint("conditions", "weekday")
    condBegin = config.getint("conditions", "begin_hour")
    condEnd = config.getint("conditions", "end_hour")
    weekday = datetime.datetime.today().weekday()
    curHour = datetime.datetime.today().hour
    
    correctTime = ( curHour >= condBegin and curHour < condEnd )
    
    if( condDay == 0 ): # any day
        return correctTime
    elif( condDay == -1 ) : # sunday 8pm to friday 3am
        return ( weekday >= 0 and weekday <= 3 ) or \
               ( weekday == 4 and curHour < 3 ) or \
               ( weekday == 6 and curHour > 20 )
    elif( condDay == -2 ) : # weekend and friday
        return ( weekday == 4 or weekday == 5 or weekday == 6 ) \
               and correctTime
    else:
        return weekday == (condDay-1) and correctTime  

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
files = [ 'OldHouse', 'Water', 'NewHouse', 'Flour', 'Bathroom' ]#[ 'timer_config' ]

InitSystem(configFolder)

while True:
    for file in files:
        config.read( configFolder + file + ".conf" )
        isActive = config.getint("conditions", "active")
        if( isActive == 0 ):
            print( "Inactive device " + file )
            continue
        unpowered = TimerCondition( config )
        print( file + " power " + ( "off" if unpowered else "on" ) )
        
        relayCnt = config.getint("relay_pins", "amount")
        for index in range(0, relayCnt) :
            pin_number = config.getint( "relay_pins", 'relay' + str( index+1 ) )
            #print( "use pin:" + str( pin_number ) )

            if( unpowered ):
                PowerOff( pin_number )
            else:
                PowerOn( pin_number )
    time.sleep( 10 )

