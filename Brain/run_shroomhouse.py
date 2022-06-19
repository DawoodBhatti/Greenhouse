#!/usr/bin/env python3

import RPi.GPIO as GPIO
import datetime
from data_processing import data_processing

#main script which can be run to take sensor readings, but also to 
#control fans, heaters and LED components in the greenhouse/shroomhouse
def run_greenhouse():

    #define variables, GPIO pin useage and GPIO numbering convention
    humidity_average = 0
    temperature_average = 0
    humidity_limit_upper = 95
    humidity_limit_lower = 80
    temperature_limit_upper = 30
    #heater_pin = 12 #ignore heater stuff for now
    humidifier_pin = 19
    fan_pin = 26
    #LED_pin = 14 #ignore LED stuff for now
    sensor_pin = 24  
    sensor_name = "greenhouse_sensor"
    #LED_scheme = "acclimatise"
    #acclimatise_from = datetime.date(2020,10,1)
    component_activation = True

    #setup pins for useage
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(heater_pin,GPIO.OUT)
    GPIO.setup(fan_pin, GPIO.OUT)
    #GPIO.setup(LED_pin, GPIO.OUT)

    #get averaged, processed sensor data
    humidity_average, temperature_average = data_processing(sensor_pin, sensor_name)
    
    #store variables as tuple
    averages = temperature_average, humidity_average
    limits = temperature_limit_upper, humidity_limit_upper, humidity_limit_lower
    pins = humidifier_pin, fan_pin
    
    #activate humidifier or fans as necessary
    if component_activation:
        temperature_and_humidity_control(averages, limits, pins)
        #LED_control(LED_pin, LED_scheme, acclimatise_from)
    
    #sleep all components at end of run
    sleep(pins)

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

#determine if activation of fans and heating is required and activate components for 2 and a half minutes
def temperature_and_humidity_control(averages, limits, pins, active_time = 150):
    
       """could optimise this code in future to employ a more intelligent solution: 
       PID stuff thingys"""
    
    #unpack tuples
    temperature_average, humidity_average = averages
    temperature_limit_upper, humidity_limit_upper, humidity_limit_lower  = limits 
    humidifier_pin, fan_pin = pins
    
    #check temperature and humidity value against limit values
    #then decide whether to operate fan and heater
    if temperature_average > temperature_limit_upper and humidity_average > humidity_limit_upper:
        print("temperature too high and humidity too high, fans on and humidifier off.")
        GPIO.output(fan_pin, GPIO.HIGH)
        GPIO.output(humidifier_pin, GPIO.LOW)
    
    elif temperature_average > temperature_limit_upper and humidity_average < humidity_limit_lower:
        print("temperature too high and humidity too low, fans on and humidifier on.")
        GPIO.output(fan_pin, GPIO.HIGH)
        GPIO.output(humidifier_pin, GPIO.HIGH)
    
    elif humidity_average < humidity_limit:
        print("humidity too low, fans off and humidifier on.")
        GPIO.output(fan_pin, GPIO.LOW)
        GPIO.output(humidifier_pin, GPIO.HIGH)
    
    return None

#a method to turn off all component pins
def sleep_greenhouse(pins):
    """find out how to shutdown the greenhouse using python"""

    humidifier_pin, fan_pin = pins
    
    GPIO.output(fan_pin, GPIO.LOW)
    GPIO.output(fan_pin, GPIO.LOW)
    GPIO.output(fan_pin, GPIO.LOW)
   
    GPIO.cleanup()
    
    return None

run_greenhouse()