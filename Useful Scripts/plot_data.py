#!/usr/bin/python
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import matplotlib.dates as md

#define file to be opened and define variables.
filedirectory = "C:/Users/dabha/Documents/Python Scripts/Raspberry Pi/projex/Greenhouse/Sensor Data/"
filedate = "15_06_2020"
filename = filedirectory + filedate + ".txt"
time_list  = []
humidity_list = []
temperature_list = []

#open file
f = open(filename, "r")
data = f.readlines()
f.close()

#extract data, format data, assign to lists
for line in data:

	time = datetime.strptime(line.split()[0], ('%H:%M:%S'))
	humidity = float(format(float(line.split()[1]), '.2f'))
	temperature = float(format(float(line.split()[2]), '.2f'))

	time_list.append(time)
	humidity_list.append(humidity)
	temperature_list.append(temperature)

#plot and format output
fig = plt.figure()
fig.suptitle("Sensor Data (" + filedate.replace("_","-") + ") : Humidity & Temperature vs. Time")
axes1 = fig.add_subplot(211)
axes2 = fig.add_subplot(212)
register_matplotlib_converters()

axes1.plot(time_list, humidity_list, linestyle =' ', marker = 'o', markersize = '1')
#axes1.title.set_text("Relative Humidity vs Time")
axes1.set_ylabel('relative humidity (%)')
axes1.set_xlabel('time (24h)')
axes1.xaxis_date()
axes1.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
#axes1.xaxis.set_major_locator(md.HourLocator(interval=1))

axes2.plot(time_list, temperature_list, linestyle =' ', marker = 'o', markersize = '1')
#axes2.title.set_text("Temperature vs Time")
axes2.set_ylabel('temperature (\u00b0C)')
axes2.set_xlabel('time (24h)')
axes2.xaxis_date()
axes2.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
#axes2.xaxis.set_major_locator(md.HourLocator(interval=1))

plt.show()