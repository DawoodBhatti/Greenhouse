#!/usr/bin/env python3

import Adafruit_DHT
from time import time, strftime, sleep

#function will collect data, save to a text file and return temperature, humidity and time
def collect_data(sensor_pin):

    #define sensor type, GPIO pin being used and variables
    sensor_type = Adafruit_DHT.DHT22
    t1 = []
    t2 = []
    y1 = []
    y2 = []
    run = 0
    data_points = 30
    date = strftime("%d_%m_%Y")

    #run the loop to collect 30 data points
    while run < data_points:
        if strftime("%d_%m_%Y") != date:
            break

        humidity, temperature = Adafruit_DHT.read_retry(sensor_type, sensor_pin)
        print (strftime("%H:%M:%S"), "\t", humidity, "%\t", temperature, "\u00b0C")

        if humidity and temperature:
            t1.append(strftime("%H:%M:%S"))
            t2.append(int(time()))
            y1.append(humidity)
            y2.append(temperature)

        sleep(2)
        run+=1

    #write to file
    filename = "/home/pi/projex/Greenhouse/Sensor Data/" + date + ".txt"
    f = open (filename, "a+")
    for i in range(len(t1)):
        f.write(str(t1[i]) + "\t" + str(y1[i]) + "\t" + str(y2[i]) + "\n")
    f.close()

    #return humidity, temperature and UTC time
    return y1, y2, t2
