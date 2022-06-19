#!/usr/bin/env python3

import RPi.GPIO as GPIO
import datetime
import subprocess
from data_processing import data_processing

#main script which can be run to take sensor readings, but also to 
#control fans, heaters and LED components in the greenhouse/shroomhouse
def run_greenhouse():

    print("begin debug")

    #define variables, GPIO pin useage and GPIO numbering convention
    humidity_average = 0
    temperature_average = 0

    humidifier_pin = 19
    fan_pin = 26
    sensor_pin = 24  
    sensor_name = "greenhouse_sensor"

    #get averaged, processed sensor data
    humidity_average, temperature_average = data_processing(sensor_pin, sensor_name)

    #setup pins for useage
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(humidifier_pin, GPIO.OUT)
    GPIO.output(humidifier_pin, GPIO.HIGH)
    GPIO.setup(fan_pin, GPIO.OUT)
    GPIO.output(fan_pin, GPIO.HIGH)


    print("finished defining variables")
    print("all done - returning none!")
    
    return None 
    
run_greenhouse()
