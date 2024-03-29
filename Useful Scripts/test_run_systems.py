#!/usr/bin/python
import Adafruit_DHT
from time import time, sleep
from run_relay import run_relay

#this code will run the humidifer, the fans and take temp/humidity readings

#define variables, sensor type and GPIO pin being used
sensor = Adafruit_DHT.DHT22
pin = 24
run = True
startTime = time()
timeLimit = 10*60
i = 0

#run the loop for 10 minutes
while run == True:
    currentTime = time()
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    print(time()-startTime, " s 	", humidity,"%	" , temperature, "\u00b0 C")

    #end loop if gone over time limit
    if currentTime-startTime >= timeLimit:
        run = False

    #run fans and humidifier every 2 minutess
    elif i ==  12:
        run_relay(10)
        i = 1

    #wait for 10 seconds before taking another reading
    else:
        sleep(10)
        i = i + 1
