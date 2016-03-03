#!/usr/bin/env python2.7
# Imanol Arrieta Ibarra
# Join reducer.
# Call: cat trip.csv fare.csv | ./join_map.py | sort | ./join_reduce.py > join.tsv

from itertools import groupby
from operator import itemgetter
import time
import sys
from math import radians, cos, sin, asin, sqrt
import json

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956  # Radius of earth in miles. Use 6371 for kms
    return c * r

def in_square(lon, lat):
    return (lon < -73.3502) and (lon > -74.5532) and (lat > 40.2858) and (lat < 41.1125)

MAX_DISTANCE = 100 # 100 miles
MAX_TIME = 86400 # one day in seconds
MAX_SPEED = 100 # miles per hour
MAX_AMOUNT = 500 # $
MAX_NPASS = 10 # maximum number of passengers

def parse_input(file, separator='\t'):
    for line in file:
        yield line.rstrip('\n').split(separator, 1)

def validate_euclidean(trip_dist,pick_long,pick_lat,drop_long,drop_lat):
    # Validate that the straight line between the pickup location and the dropoff location is shorter
    # than the trip distance.
    # Get distance in miles between GPS points
    distance_gps = haversine(pick_long, pick_lat, drop_long, drop_lat)
    # check if distance computed with haversine is smaller might want to include confidence interval.
    return distance_gps <= trip_dist

def validate_gps(lon,lat):
    return in_square(lon, lat)

def validate_distance(trip_dist,pick_long,pick_lat,drop_long,drop_lat):
    distance_gps = haversine(pick_long, pick_lat, drop_long, drop_lat)
    distance_gps_valid = distance_gps > 0 and distance_gps <= MAX_DISTANCE
    distance_trip_valid = trip_dist > 0 and trip_dist <= MAX_DISTANCE
    return distance_gps_valid and distance_trip_valid

def validate_time(time):
    # Time is greater than zero and is not too extreme
    return time > 0 and time < MAX_TIME

def validate_velocity(time,trip_dist):
    if time == 0:
        return False
    # Velocity is positive and not too extreme
    time_hours = time / 3600.0
    average_speed = trip_dist/time_hours # mi/hr
    return average_speed > 0 and average_speed < MAX_SPEED

def validate_amount(amount):
    # Amount is greater than zero and not too extreme.
    return amount > 0 and amount < MAX_AMOUNT

def validate_passengers(n_pass):
    # Amount is greater than zero and not too extreme.
    return n_pass>0 and n_pass<MAX_NPASS

def validate_data(info):

    hack_license,pick_datetime,drop_datetime,n_passengers,trip_dist,pick_long,\
    pick_lat,drop_long,drop_lat,payment_type,fare_amount,\
    surcharge,tip_amount,mta_tax,tolls_amount,total_amount=info

    time_in_seconds = time.mktime(time.strptime(drop_datetime,'%Y-%m-%d %H:%M:%S'))-\
                      time.mktime(time.strptime(pick_datetime,'%Y-%m-%d %H:%M:%S'))
    try:
        pick_long = float(pick_long)
        pick_lat = float(pick_lat)
        drop_long = float(drop_long)
        drop_lat = float(drop_lat)
        trip_dist = float(trip_dist)
        total_amount = float(total_amount)
        time_in_seconds = float(time_in_seconds)
        n_passengers = int(n_passengers)
    except ValueError:
        return False
    # Is the straight distance shorter than the reported distance?
    euclidean = validate_euclidean(trip_dist,pick_long,pick_lat,drop_long,drop_lat)
    gps_pickup = validate_gps(pick_long,pick_lat) # Are the GPS coordinates present in Manhattan
    gps_dropoff = validate_gps(drop_long,drop_lat)
    distance = validate_distance(trip_dist,pick_long,pick_lat,drop_long,drop_lat) # Are distances too big
    val_time = validate_time(time_in_seconds) # Are times too long or 0? Are they positive?
    velocity = validate_velocity(time_in_seconds,trip_dist) # Is velocity too out of reach
    amount = validate_amount(total_amount)
    pass_validate = validate_passengers(n_passengers)
    return(euclidean and gps_pickup and gps_dropoff and distance and val_time and velocity and amount and pass_validate)

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



