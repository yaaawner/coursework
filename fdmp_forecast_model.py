from forecast import drift_moving_average
from forecast import learning
import math

ALPHA = 100
#TODO: io with files

buf_rate = [55000, 50000, 49000, 46789, 26789, 10920, 20000, 30000, 20000, 40000] #input from file
rtt = 100
cwnd = 4000
step = 100
requirement = 45000
buffer = []

time = 0
open_subflow_flag = False

difrate = 0
difstep = 0
index_inc_rate = 0
k = 1

i = 0
for rate in buf_rate:
    buffer.append(rate)
    if i < 100:
        i += 1
    else:
        i = 0
    time += step
    time_to_open_subflow = (2 + math.log(cwnd, 2)) * rtt
    #print(time_to_open_subflow)
    prediction = drift_moving_average(buffer, step, k, rtt, cwnd)

    if time_to_open_subflow < step:
        pred = 1
    else:
        pred = time_to_open_subflow // step

    index = (i + pred) % 100
    #forecast_list[i + pred] = drift_moving_average(buf_rate, step, k, rtt, cwnd)

    if open_subflow_flag:
        rate += difstep * index_inc_rate
        index_inc_rate += 1
        #print(rate)

    elif prediction + ALPHA < requirement:
        #print("drift", drift_moving_average(buf_rate, step, k, rtt, cwnd))
        difrate = (requirement - prediction)
        difstep = difrate // pred
        open_subflow_flag = True
        index_inc_rate = 1

    elif rate + ALPHA < requirement:
        difrate = requirement - rate
        difstep = difrate // pred
        open_subflow_flag = True
        index_inc_rate = 1
        k = learning(buffer, step, k, rtt, cwnd, rate)

    if rate > requirement:          #!!!
        open_subflow_flag = False

    print(time, rate)