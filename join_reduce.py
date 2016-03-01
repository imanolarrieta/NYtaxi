#!/usr/bin/env python2.7
# Imanol Arrieta Ibarra
# Join reducer.
# cat trip.csv fare.csv | ./join_map.py | sort | ./join_reduce.py > join.tsv

from itertools import groupby
from operator import itemgetter
import sys

def parse_input(file, separator='\t'):
    for line in file:
        yield line.rstrip('\n').split(separator, 1)

def validate_euclidean(distance,long_pick,lat_pick,long_drop,lat_drop):
    pass
def validate_gps(long,lat):
    pass
def validate_distance(distance):
    pass
def validate_time(time):
    pass
def validate_velocity(velocity):
    pass
def validate_amount(velocity):
    pass

def validate_data(info):

    euclidean = validate_euclidean(info) # Is the straight distance shorter than the reported distance?
    gps_pickup = validate_gps(info) # Are the GPS coordinates present in Manhattan
    gps_dropoff = validate_gps(info)
    distance = validate_distance(info) # Are distances too big
    time = validate_time(info) # Are times too long or 0
    velocity = validate_velocity(info) # Is velocity too out of reach
    amount = validate_amount(info)

    return(True)

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



