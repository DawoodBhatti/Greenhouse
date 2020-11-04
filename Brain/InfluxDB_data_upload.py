#!/usr/bin/env python3

from influxdb import InfluxDBClient
from time import time, sleep

#uploads data to database within InfluxDB, specified by db_name
def InfluxDB_data_upload(location="default", humidity=[12,31,14,15,16,17,13], temperature=[18,17,16,17,17,18,18], timestamp=[]):

    #initialise variables
    database_name = "greenhouse"
    measurement = "m1"

    #check data supplied is as expected
    if len(humidity) != len(temperature):
        print ("humidity and temperature lists are not of equal length, please fix this")
        return None
    elif len(humidity) == 0:
        print ("lists supplied are empty of data, please fix this")

    #populate timestamp list if none was provided
    if len(timestamp)==0:
        for i in range(0,len(humidity)+1):
            timestamp.append(int(time()))
            sleep(1)

    #connect to InfluxDB, connect to database specified 
    print("connecting to database client... logging in...")
    client = InfluxDBClient(host='localhost', port=8086, username='admin', password='<7725pi>')
    print("using database: " + database_name)
    client.switch_database(database_name)

    #create a list of strings containing data and associated metadata
    data_list = ["{me},location={lo} temperature={te},humidity={hu} {ti}"
                    .format(me=measurement,
                            lo=location,
                            te=temperature[x],
                            hu=humidity[x],
                            ti=timestamp[x]) for x in range(0,len(humidity))]

    #write data_list to database and congratulate the user on a job well done
    print("writing " + measurement + " to database: " + database_name)
    client.write_points(data_list, database=database_name, time_precision='s', batch_size=5000, protocol='line')
    print("good job. write complete.")

    return None

#InfluxDB_data_upload()
