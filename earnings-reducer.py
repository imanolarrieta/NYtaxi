#!/usr/bin/env python2.7
# Imanol Arrieta Ibarra
# Earnings reducer
# Call : cat trip.csv fare.csv | ./join_map.py
# fare.csv has lines of length 11 and is the right dataset. trip.csv has lines of lenght 14.
# Key: hack_license
# Value: pick_datetime,drop_datetime,trip_dist,pick_long,pick_lat,drop_long,drop_lat,payment_type,fare_amount,
# surcharge,tip_amount,mta_tax,tolls_amount,total_amount

from itertools import groupby
from operator import itemgetter
from time import mktime
from datetime import datetime, timedelta
import sys

def parse_input(file, separator='\t'):
    for line in file:
        yield line.rstrip('\n').split(separator, 1)

def time_diff(t1,t2):
    #Computes the difference between t2 and t1 in seconds. t2 and t1 are datetime objects.
    return mktime(t1.timetuple())-mktime(t2.timetuple())

# We want to compute per hour and per driver a number of different statistics.
# All these statistics are for trips that started in that hour
# 1) time_on_duty: We will compute this statistic under multiple assumptions.
#     a) We will assume that as long as a driver works in an hour they are active. _faber
#     b) We will assume that time with no passenger longer than 30 minutes is a break. _30
#     c) We will assume that time with no passenger longer than 15 minutes is a break. _15
#     d) We will assume that time with no passenger longer than 1 hour is a break. _60
# 2) t_occupied: The total amount of time with passenger during that hour
# 3) n_pass: Number of passengers picked up during that hour
# 4) n_trip: Number of trips started during that hour
# 5) n_miles: Number of miles traveled with passengers during that hour.
# 6) av_speed: Average of average speed for that hour.
# 7) earnings: Total earnings for that hour
# 8) tips: Total tips for that hour

data = parse_input(sys.stdin)
for key, values in groupby(data, itemgetter(0)):
    t_onduty_faber = 3600
    t_onduty_15,t_onduty_30,t_onduty_60,t_occupied,n_pass,n_trip,\
      n_miles,av_speed,earnings_card,earnings_cash,tips_card,tips_cash,fare,time_unoccupied  = 14*[0]
    goes_over = False
    last_dropoff = []
    current_hour = []
    for value in values:
        # Unpack values
        hack_license,pick_date,drop_date,passengers,trip_dist,pick_long,\
        pick_lat,drop_long,drop_lat,payment_type,fare_amount,\
        surcharge,tip_amount,mta_tax,tolls_amount,total_amount = value[1].split('\t')

        pick_date = datetime.strptime(pick_date,'%Y-%m-%d %H:%M:%S')
        drop_date = datetime.strptime(drop_date,'%Y-%m-%d %H:%M:%S')
        pick_hour = pick_date.replace(minute=0,second=0)
        drop_hour = drop_date.replace(minute=0,second=0)
        trip_time = time_diff(drop_date,pick_date)

        if not current_hour:
            current_hour.append(pick_hour)
        elif time_diff(pick_hour,current_hour[0])>0:
            hour_stats= [pick_hour.strftime('%Y-%m-%d %H'),\
                    current_hour.pop().hour,pick_date.date().strftime('%Y-%m-%d'),
                    hack_license,t_onduty_faber,t_onduty_15,t_onduty_30,t_onduty_60,t_occupied,n_pass,n_trip,\
                    n_miles,av_speed,earnings_card,earnings_cash,tips_card,tips_cash,fare,goes_over]
            print '\t'.join([str(x) for x in hour_stats])
            current_hour.append(pick_hour) # Change hour aggregation
            # Reinitialize hour variables
            t_onduty_15,t_onduty_30,t_onduty_60,t_occupied,n_pass,n_trip,\
            n_miles,av_speed,earnings_card,earnings_cash,tips_card,tips_cash,fare,time_unoccupied  = 14*[0]
            goes_over= False

        second_earnings = float(total_amount)/float(trip_time)

        goes_over = time_diff(drop_hour,pick_hour)>0 # Does the trip goes over an hour

        if last_dropoff:
            time_unoccupied += time_diff(pick_date,last_dropoff.pop())
        last_dropoff.append(drop_date)

        t_onduty_15 += time_unoccupied + trip_time if time_unoccupied<900 else trip_time
        t_onduty_30 += time_unoccupied + trip_time if time_unoccupied<1800 else trip_time
        t_onduty_60 += time_unoccupied + trip_time if time_unoccupied<3600 else trip_time
        t_occupied += trip_time
        n_pass += passengers
        n_trip += 1
        n_miles += trip_dist
        av_speed +=











    hour_stats= [pick_hour.strftime('%Y-%m-%d %H'),current_hour.pop().hour,pick_date.date().strftime('%Y-%m-%d'),
                    hack_license,t_onduty_faber,t_onduty_15,t_onduty_30,t_onduty_60,t_occupied,n_pass,n_trip,\
                    n_miles,av_speed,earnings_card,earnings_cash,tips_card,tips_cash,fare,goes_over]
    print '\t'.join([str(x) for x in hour_stats])





