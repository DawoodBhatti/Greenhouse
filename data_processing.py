#!/usr/bin/env python3

from InfluxDB_data_upload import InfluxDB_data_upload
from collect_data import collect_data

#function filters and averages data gathered from sensor. also uploads to InfluxDB.
#returns averaged humidity and temperature from reading
def data_processing(sensor_pin):

    #define variables
    humidity_average = 0
    temperature_average = 0

    #collect data from sensor
    humidity, temperature, time_UTC = collect_data(sensor_pin)
    
    if len(humidity)==0 or len(temperature)==0 or len(time_UTC)==0:
        print("empty lists have been passed to data_processing function. please fix")
        return None
        
    humidity_average = sum(humidity)/len(humidity)
    temperature_average = sum(temperature)/len(temperature)

    """future improvement: could scrub data for any instances of points which are clearly incorrect results. Such as 3000% humidity and a 10c 
    temperature result. Not sure how to improve these just yet"""

    #upload data to InfluxDB
    InfluxDB_data_upload("sandwich_box", humidity, temperature, time_UTC)
    
    return humidity_average, temperature_average
