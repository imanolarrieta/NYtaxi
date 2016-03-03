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
    agg_duty_faber = 0.0
    agg_occupied = 0.0
    agg_earnings = 0.0
    agg_hack = 0.0
    agg_rides=0.0

    for value in values:

        hour,date,hack_license,t_onduty_faber,t_onduty_15,t_onduty_30,t_onduty_60,t_occupied,n_pass,n_trip,\
        n_miles,av_speed,earnings_card,earnings_cash,tips_card,tips_cash,fare,goes_over= value[1].split('\t')

        agg_duty_15+= float(t_onduty_15)
        agg_duty_30+= float(t_onduty_30)
        agg_duty_60+= float(t_onduty_60)
        agg_duty_faber+= float(t_onduty_faber)

        agg_occupied += float(t_occupied)
        agg_passengers += float(n_pass)
        agg_earnings += float(total_earned)
        agg_hack +=1
        agg_rides+=float(num_rides)

    print '\t'.join([key,str(agg_duty_15),str(agg_duty_30),str(agg_duty_60),str(agg_duty_360),
                     str(agg_occupied),str(agg_earnings),str(agg_hack),str(agg_rides)])


