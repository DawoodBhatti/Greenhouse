#!/usr/bin/env python3

import RPi.GPIO as GPIO
from data_processing import data_processing

#use processed sensor data to control fan and heater components
def run():

    #define variables, GPIO pin useage and GPIO numbering convention
    humidity_average = 0
    humidity_limit = 0
    temperature_average = 0
    temperature_limit = 30
    fan_pin = 0
    heater_pin = 14
    sensor_pin = 4

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(heater_pin,GPIO.OUT)

    #get processed sensor data
    humidity_average, temperature_average = data_processing(sensor_pin)


    """could optimise these values in future to have a window of equilibrium. e.g. stop above 1.02 * temp and start below 0.98 * temp"""
    #check temperature value against limit values, operate fan and heater as required
    if temperature_average > temperature_limit:
        print("temperature limit exceeded, cooling required")
        GPIO.output(heater_pin, GPIO.LOW)
        #GPIO.output(fan_pin, GPIO.HIGH)
        GPIO.cleanup()


    else:
        GPIO.output(heater_pin, GPIO.HIGH)
        #GPIO.output(fan_pin, GPIO.HIGH)


run()


