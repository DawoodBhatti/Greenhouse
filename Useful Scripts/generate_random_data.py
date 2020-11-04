# -*- coding: utf-8 -*-

#this code will need to be modified so that the raspberry pi writes into a new file when the date is different?
#a test to see if the currentDate is the same as the previous date
#if false, loop breaks and creates new file?

from datetime import datetime
import random

currentTime = datetime.now().strftime("%H:%M:%S")
currentDate = datetime.now().strftime("%d_%m_%Y")
time = []
humidity = []
temp = []

filename = "C:\\Users\\dabha\\Documents\\Python Scripts\\Raspberry Pi\\sensor data " + currentDate + ".txt"
file = open(filename, "a+")

for i in range (0, 2000):
    humidity = random.uniform(70, 85)
    temp = random.uniform(18, 21)
    file.write(str(currentTime) + "\t" )
    file.write(str(humidity) + "\t" )
    file.write(str(temp) + "\n")

file.close()
