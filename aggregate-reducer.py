#!/usr/bin/python
from itertools import groupby
from operator import itemgetter
import sys

def parse_input(file, separator='\t'):
    for line in file:
        yield line.rstrip('\n').split(separator, 1)


data = parse_input(sys.stdin)
for key, values in groupby(data, itemgetter(0)):
    agg_duty_15 = 0.0
    agg_duty_30 = 0.0
    agg_duty_60 = 0.0
    agg_duty_360 = 0.0
    agg_occupied = 0.0
    agg_earnings = 0.0
    agg_hack = 0.0
    agg_rides=0.0

    for value in values:
        time_on_duty_15,time_on_duty_30,time_on_duty_60,time_on_duty_360,time_occupied,total_earned, num_rides = value[1].split('\t')
        agg_duty_15+= float(time_on_duty_15)
        agg_duty_30+= float(time_on_duty_30)
        agg_duty_60+= float(time_on_duty_60)
        agg_duty_360+= float(time_on_duty_360)

        agg_occupied += float(time_occupied)
        agg_earnings += float(total_earned)
        agg_hack +=1
        agg_rides+=float(num_rides)

    print '\t'.join([key,str(agg_duty_15),str(agg_duty_30),str(agg_duty_60),str(agg_duty_360),
                     str(agg_occupied),str(agg_earnings),str(agg_hack),str(agg_rides)])


