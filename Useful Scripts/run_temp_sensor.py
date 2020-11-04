#!/usr/bin/python
import Adafruit_DHT
from time import time, sleep

#define variables, sensor type and GPIO pin being used
sensor = Adafruit_DHT.DHT22
pin = 4
run = True
startTime = time()

#run the loop for 3600 seconds (1 hour)
while run == True:
    currentTime = time()
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    print(time()-startTime, " s 	", humidity,"%	" , temperature, "\u00b0 C")

    if currentTime-startTime >= 3600:
        run = False
    else:
        sleep(15)
