#!/usr/bin/env python2.7
# Imanol Arrieta Ibarra
# Join mapper.
# Call : cat trip.csv fare.csv | ./join_map.py
# fare.csv has lines of length 11 and is the right dataset. trip.csv has lines of lenght 14.

import sys

def join_map():
    for line in sys.stdin:
        values = line.rstrip('\n').rstrip('\r').split(',')
        if values[0]=='medallion': #First line is the header.
            continue

        if len(values) == 11:
            medallion, hack_license, vender_id, \
            pickup_datetime, payment_type, \
            fare_amount, surcharge, mta_tax, tip_amount, \
            tolls_amount, total_amount = values

            print '\t'.join([hack_license+pickup_datetime,payment_type,fare_amount,\
                             surcharge,tip_amount,mta_tax,tolls_amount,total_amount,'right'])
        elif len(values)==14:
            medallion, hack_license, vender_id, \
            rate_code, fwd_flag,pickup_datetime, dropoff_datetime,\
            passenger_count, trip_time_in_secs, trip_distance, \
            pickup_longitude,pickup_latitude, \
            dropoff_longitude, dropoff_latitude = values

            print '\t'.join([hack_license+pickup_datetime,hack_license,pickup_datetime,\
                             dropoff_datetime,passenger_count,trip_distance,pickup_longitude,\
                             pickup_latitude,dropoff_longitude,dropoff_latitude,'left'])

if __name__=='__main__':
    join_map()