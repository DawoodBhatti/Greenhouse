#!/usr/bin/env python3

import RPi.GPIO as GPIO
import datetime
import configparser
from data_processing import data_processing

#main script which can be run to take sensor readings, but also to 
#control fans, heaters and LED components in the greenhouse
def run_greenhouse():

    #import variables from config.ini
    config = configparser.ConfigParser()
    path = "C:/Users/dabha/Documents/GitHub/Greenhouse/Brain/"    
    file = "config.ini"
    config.read((path+file))

    #read variables, define GPIO pin useage and define GPIO numbering convention
    humidity_average     =   float(config['devpi01_greenhouse']['humidity_average'])
    temperature_average  =   float(config['devpi01_greenhouse']['temperature_average'])
    humidity_limit       =   float(config['devpi01_greenhouse']['humidity_limit'])
    temperature_limit    =   float(config['devpi01_greenhouse']['temperature_limit'])
    heater_pin           =   int(config['devpi01_greenhouse']['heater_pin'])
    fan_pin              =   int(config['devpi01_greenhouse']['fan_pin'])
    LED_pin              =   int(config['devpi01_greenhouse']['LED_pin'])
    sensor_pin           =   int(config['devpi01_greenhouse']['sensor_pin'])
    sensor_name          =   str(config['devpi01_greenhouse']['sensor_name'])
    LED_scheme           =   str(config['devpi01_greenhouse']['LED_scheme'])
    acclimatise_from     =   datetime.date(int(config['devpi01_greenhouse']['acclimatise_from_year']),
                                           int(config['devpi01_greenhouse']['acclimatise_from_month']),
                                           int(config['devpi01_greenhouse']['acclimatise_from_day']))
    component_activation =   config.getboolean('devpi01_greenhouse', 'component_activation')

    #setup pins for useage
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(heater_pin,GPIO.OUT)
    GPIO.setup(fan_pin, GPIO.OUT)
    GPIO.setup(LED_pin, GPIO.OUT)

    #get averaged, processed sensor data
    humidity_average, temperature_average = data_processing(sensor_pin, sensor_name)
    
    #store variables as tuple
    averages = temperature_average, humidity_average
    limits = temperature_limit, humidity_limit
    pins = heater_pin, fan_pin
    
    #activate heater, fan and LED components if necessary
    if component_activation:
        temperature_and_humidity_control(averages, limits, pins)
        LED_control(LED_pin, LED_scheme, acclimatise_from)

    return None

#activate the lighting with acclimatise scheme or regular scheme
def LED_control(LED_pin, LED_scheme, acclimatise_from = None):
    
    #lighting starts at 8am for both schemes
    start_date = acclimatise_from
    start_time = datetime.time(8,0)
    max_active_time = datetime.timedelta(minutes = 60 * 12)
    date_today = datetime.date.today()
    current_time = datetime.datetime.now()
    
    #check if the time is before desired LED start time 
    if current_time < datetime.datetime.combine(date_today, start_time):
        GPIO.output(LED_pin, GPIO.LOW)
        return None
    
    #check if the time is after desired LED finish time
    elif current_time > (datetime.datetime.combine(date_today, start_time) + max_active_time):
        GPIO.output(LED_pin, GPIO.LOW)
        return None
    
    #store variables as tuple
    times = start_time, current_time, max_active_time
    dates = start_date, date_today
    
    #call appropriate function
    if LED_scheme == "acclimatise":
        LED_acclimatise_scheme(LED_pin, times, dates)
    elif LED_scheme =="regular":
        LED_regular_scheme(LED_pin, times, dates)
    else:
        print ("the LED lighting scheme has been incorrectly specified")

    return None

#run the LED according to a scheme which acclimatises plants to the lighting.
#acclimatise scheme lighting starts at 8am and operates 10 minutes for each day
#past the acclimatise_from date, up to a current maximum active time of 12 hours 
def LED_acclimatise_scheme(LED_pin, times, dates):
    
    #unpack tuples and calculate difference between dates
    start_time, current_time, max_active_time = times
    start_date, date_today = dates 
    difference = (date_today - start_date).days
        
    if start_date == None:
        print ("a start date must be provided to use the acclimatise scheme")
        return None
    
    if difference < 0:
        print("you have incorrectly selected a future date as the acclimatisation start date")
        return None
        
    #calculate LED operating time
    operating_time = datetime.timedelta(minutes = 10 * difference) 
    if operating_time > max_active_time:
        operating_time = max_active_time
            
    #calculate start time and finish time 
    finish_time = datetime.datetime.combine(date_today, start_time) + operating_time
    start_time = datetime.datetime.combine(date_today, start_time)

    #operate LED if time is after desired start time and before desired finish time
    if current_time > start_time and current_time < finish_time:
        GPIO.output(LED_pin, GPIO.HIGH)
        
    return None

#run the LED according to regular scheme. lighting starts at 8am and stops at 8pm
def LED_regular_scheme(LED_pin, times, dates):
        
    #unpack tuples and calculate difference between dates
    start_time, current_time, max_active_time = times
    start_date, date_today = dates 
        
    start_time = datetime.datetime.combine(start_time, date_today)
    finish_time = datetime.datetime.combine(start_time,date_today) + max_active_time

    #calculate LED operating time, start time and finish time 
    operating_time = max_active_time
    finish_time = datetime.datetime.combine(date_today, start_time) + operating_time
    start_time = datetime.datetime.combine(date_today, start_time)
    
    #operate LED if time is after desired start time and before desired finish time
    if current_time > start_time and current_time < finish_time:
        GPIO.output(LED_pin, GPIO.HIGH)
    
    return None

#determine if activation of fans and heating is required
def temperature_and_humidity_control(averages, limits, pins):
    
    #unpack tuples
    temperature_average, humidity_average = averages
    temperature_limit, humidity_limit = limits 
    heater_pin, fan_pin = pins
    
    """could optimise these values in future to have a window of equilibrium.
    e.g. stop above 1.02 * temp and start below 0.98 * temp.
    Can also look up PID stuff thingys here"""
    
    #check temperature value against limit values, operate fan and heater as required
    if temperature_average > temperature_limit and humidity_average > humidity_limit:
        print("temperature too high and humidity too high, fans on and heater off.")
        GPIO.output(fan_pin, GPIO.HIGH)
        GPIO.output(heater_pin, GPIO.LOW)

    elif temperature_average > temperature_limit and humidity_average < humidity_limit:
        print("temperature too high and humidity too low, fans on and heater off.")
        GPIO.output(fan_pin, GPIO.HIGH)
        GPIO.output(heater_pin, GPIO.LOW)

    elif temperature_average < temperature_limit and humidity_average > humidity_limit:
        print("temperature too low and humidity too high, fans on and heater on ")
        GPIO.output(fan_pin, GPIO.HIGH)
        GPIO.output(heater_pin, GPIO.HIGH)
    
    elif temperature_average < temperature_limit and humidity_average < humidity_limit:
        print("temperature too low and humidity too low, fans off and heater on.")
        GPIO.output(fan_pin, GPIO.LOW)
        GPIO.output(heater_pin, GPIO.HIGH)

    return None

#a method to turn off all pins and shutdown the greenhouse
def sleep_greenhouse(pins, LED_pin):
    heater_pin, fan_pin = pins
    
    GPIO.output(fan_pin, GPIO.LOW)
    GPIO.output(fan_pin, GPIO.LOW)
    GPIO.output(fan_pin, GPIO.LOW)

    """find out how to shutdown the greenhouse using python"""
    
    GPIO.cleanup()
    
    return None

run_greenhouse()