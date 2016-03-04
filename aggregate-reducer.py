#!/usr/bin/python
from itertools import groupby
from operator import itemgetter
import sys

def parse_input(file, separator='\t'):
    for line in file:
        yield line.rstrip('\n').split(separator, 1)


data = parse_input(sys.stdin)
for key, values in groupby(data, itemgetter(0)):
    agg_duty_15,agg_duty_30, agg_duty_60,agg_duty_faber,agg_occupied,agg_hack,agg_trips,\
       agg_pass,agg_miles,agg_speed,agg_earnings_card,agg_earnings_cash,agg_tips_card,\
       agg_tips_cash,agg_fare,agg_goes_over= 16*[0.0]

    for value in values:

        hour,date,hack_license,t_onduty_faber,t_onduty_15,t_onduty_30,t_onduty_60,t_occupied,n_pass,n_trip,\
        n_miles,av_speed,earnings_card,earnings_cash,tips_card,tips_cash,fare,goes_over= value[1].split('\t')

        agg_duty_15+= float(t_onduty_15)
        agg_duty_30+= float(t_onduty_30)
        agg_duty_60+= float(t_onduty_60)
        agg_duty_faber+= float(t_onduty_faber)
        agg_occupied += float(t_occupied)
        agg_pass += float(n_pass)
        agg_hack +=1
        agg_trips += float(n_trip)
        agg_miles += float(n_miles)
        agg_speed += float(av_speed)
        agg_earnings_card += float(earnings_card)
        agg_earnings_cash += float(earnings_cash)
        agg_tips_card += float(earnings_card)
        agg_tips_cash += float(earnings_cash)
        agg_fare += float(fare)
        agg_goes_over += float(bool(goes_over))

    print '\t'.join([key,str(agg_duty_15),str(agg_duty_30),str(agg_duty_60),str(agg_duty_faber),
                     str(agg_occupied),str(agg_pass),str(agg_hack),str(agg_trips),str(agg_miles),
                     str(agg_speed),str(agg_earnings_card),str(agg_earnings_cash),str(agg_tips_card),
                     str(agg_tips_cash),str(agg_fare),str(agg_goes_over)])


