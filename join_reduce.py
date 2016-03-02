#!/usr/bin/env python2.7
# Imanol Arrieta Ibarra
# Join reducer.
# Call: cat trip.csv fare.csv | ./join_map.py | sort | ./join_reduce.py > join.tsv

from itertools import groupby
from operator import itemgetter
import time
import sys

def parse_input(file, separator='\t'):
    for line in file:
        yield line.rstrip('\n').split(separator, 1)

def validate_euclidean(trip_dist,pick_long,pick_lat,drop_long,drop_lat):
    # Validate that the straight line between the pickup location and the dropoff location is shorter
    # than the trip distance.
    pass

def validate_gps(long,lat):
    # Validate that longitude and latitude are valid values. (In an area that surrounds Manhattan)
    pass

def validate_distance(trip_dist,pick_long,pick_lat,drop_long,drop_lat):
    # Distances are positive, greater than zero and not too extreme.
    pass
def validate_time(time_in_seconds):
    # Time is greater than zero and is not too extreme
    pass

def validate_velocity(velocity):
    # Velocity is positive and not too extreme
    pass
def validate_amount(amount):
    # Amount is greater than zero and not too extreme.
    pass

def validate_data(info):

    hack_license,pick_datetime,drop_datetime,trip_dist,pick_long,\
    pick_lat,drop_long,drop_lat,payment_type,fare_amount,\
    surcharge,tip_amount,mta_tax,tolls_amount,total_amount=info

    time_in_seconds = time.mktime(time.strptime(drop_datetime,'%Y-%m-%d %H:%M:%S'))-\
                      time.mktime(time.strptime(pick_datetime,'%Y-%m-%d %H:%M:%S'))

    # Is the straight distance shorter than the reported distance?
    euclidean = validate_euclidean(trip_dist,pick_long,pick_lat,drop_long,drop_lat)
    gps_pickup = validate_gps(pick_long,pick_lat) # Are the GPS coordinates present in Manhattan
    gps_dropoff = validate_gps(drop_long,drop_lat)
    distance = validate_distance(trip_dist,pick_long,pick_lat,drop_long,drop_lat) # Are distances too big
    val_time = validate_time(info) # Are times too long or 0? Are they positive?
    velocity = validate_velocity(time_in_seconds) # Is velocity too out of reach
    amount = validate_amount(total_amount)
    return(euclidean and gps_pickup and gps_dropoff and distance and val_time and velocity and amount)

data = parse_input(sys.stdin)
for key, values in groupby(data, itemgetter(0)):
    joined_data = {}
    for value in values:
        variables = value[1].split('\t')
        joined_data[variables[-1]]= variables[:-1]
    if ('left' in joined_data and 'right' in joined_data):
        all_data = joined_data['left']+joined_data['right']
        if validate_data(all_data):
            print '\t'.join(all_data)



