#!/usr/bin/python
from itertools import groupby
from operator import itemgetter
from datetime import datetime
from datetime import timedelta
from time import mktime
import sys

def parse_input(file, separator='\t'):
    for line in file:
        yield line.rstrip('\n').split(separator, 1)

def time_diff(t1,t2):
    return mktime(t1.timetuple())-mktime(t2.timetuple())

data = parse_input(sys.stdin)
for key, values in groupby(data, itemgetter(0)):
    taxi_driver =[]
    for value in values:
        pickup_date, dropoff_date, trip_time_in_secs,total_amount = value[1].split('\t')
        pickup_date = datetime.strptime(pickup_date,'%Y-%m-%d %H:%M:%S')
        dropoff_date = datetime.strptime(dropoff_date,'%Y-%m-%d %H:%M:%S')
        pickup_hour = pickup_date.replace(minute=0,second=0)
        dropoff_hour = dropoff_date.replace(minute=0,second=0)
        trip_time_in_secs = time_diff(dropoff_date,pickup_date)
        if trip_time_in_secs>0:
            second_earnings = float(total_amount)/float(trip_time_in_secs)
        else:
            second_earnings = 0


        while(dropoff_hour>pickup_hour):
            new_dropoff_date = (pickup_date+timedelta(hours=1)).replace(minute=0,second=0)
            new_amount = second_earnings*time_diff(new_dropoff_date,pickup_date)
            taxi_driver.append([pickup_hour,pickup_date,new_dropoff_date,new_amount])
            pickup_date = new_dropoff_date
            pickup_hour = pickup_date.replace(minute=0,second=0)

        new_amount = second_earnings*time_diff(dropoff_date,pickup_date)
        taxi_driver.append([pickup_hour,pickup_date,dropoff_date,new_amount])

    taxi_driver = sorted(taxi_driver,key = itemgetter(1),reverse=False)

    time_occupied = 0
    time_on_duty_15 = 0
    time_on_duty_30 = 0
    time_on_duty_60 = 0
    time_on_duty_360 = 0
    total_earned = 0
    num_rides = 0
    last_dropoff = datetime.strptime('1970-01-01 00:00:01','%Y-%m-%d %H:%M:%S')
    last_hour  = taxi_driver[0][0]

    for ride in taxi_driver:
        hour,pickup,dropoff,amount = ride
        if (hour>last_hour):
            print '\t'.join([str(last_hour),str(time_on_duty_15),
                             str(time_on_duty_30),str(time_on_duty_60),str(time_on_duty_360),
                             str(time_occupied),str(total_earned),str(num_rides)])
            total_earned = 0
            time_occupied =0
            time_on_duty_15 = 0
            time_on_duty_30 = 0
            time_on_duty_60 = 0
            time_on_duty_360 = 0
            num_rides=0

        time_unoccupied = time_diff(pickup,last_dropoff)/60
        if (time_unoccupied<15):
            time_on_duty_15+=time_unoccupied
            time_on_duty_30+=time_unoccupied
            time_on_duty_60+=time_unoccupied
            time_on_duty_360+=time_unoccupied
        elif (time_unoccupied<30):
            time_on_duty_30+=time_unoccupied
            time_on_duty_60+=time_unoccupied
            time_on_duty_360+=time_unoccupied
        elif (time_unoccupied<60):
            time_on_duty_60+=time_unoccupied
            time_on_duty_360+=time_unoccupied
        elif (time_unoccupied<360):
            time_on_duty_360+=time_unoccupied

        num_rides +=1
        time_ride = time_diff(dropoff,pickup)
        time_occupied+=time_ride
        time_on_duty_15+=time_ride
        time_on_duty_30+=time_ride
        time_on_duty_60+=time_ride
        time_on_duty_360+=time_ride
        total_earned+= amount
        last_dropoff = dropoff
        last_hour = hour

    print '\t'.join([str(last_hour),str(time_on_duty_15),
                             str(time_on_duty_30),str(time_on_duty_60),str(time_on_duty_360),
                             str(time_occupied),str(total_earned),str(num_rides)])





