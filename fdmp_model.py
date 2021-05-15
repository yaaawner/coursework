from forecast import drift_moving_average
from forecast import learning
import math

ALPHA = 100
#TODO: io with files

buf_rate = [] #input from file
rtt = 0
cwnd = 0
step = 0
requirement = 0

time = 0
open_subflow_flag = False

difrate = 0
difstep = 0

index_inc_rate = 0

i = 0
for rate in buf_rate:
    if i < 100:
        i += 1
    else:
        i = 0
    time += step
    time_to_open_subflow = (2 + math.log(cwnd, 2)) * rtt

    if time_to_open_subflow < step:
        pred = 1
    else:
        pred = time_to_open_subflow // step

    if open_subflow_flag:
        rate += difstep * index_inc_rate
        index_inc_rate += 1

    elif rate + ALPHA < requirement:
        difrate = (rate - requirement)
        difstep = difrate // pred
        open_subflow_flag = True
        index_inc_rate = 1

    if rate > requirement:
        open_subflow_flag = False

    print(time, rate)