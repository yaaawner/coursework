from forecast import drift_moving_average
from forecast import learning
import math

ALPHA = 100
#TODO: io with files, open subflow, close subflow, change rate

buf_rate = []
rtt = 0
cwnd = 0
step = 0
requirement = 0
FT = []
TT = []
time = 0
forecast_list = [requirement+100 for j in range(100)]
k = 3

open_subflow_flag = False
#TODO: 1,5 RTT, slowstart (linear for simple, but need to calculate time)

i = 0
for rate in buf_rate:
    if i < 100:
        i += 1
    else:
        i = 0

    time += step
    h = (2 + math.log(cwnd, 2)) * rtt
    if h < step:
        pred = 1
    else:
        pred = h // step

    index = (i + pred) % 100
    forecast_list[i + pred]=drift_moving_average(buf_rate, step, k, rtt, cwnd)

    if rate < requirement - ALPHA and requirement - ALPHA < forecast_list[i]:
        k = learning(buf_rate, step, k, rtt, cwnd, rate)
        FT.append(time)
    elif rate < requirement - ALPHA and forecast_list[i] < requirement - ALPHA:
        TT.append(time)

    print(time, rate, forecast_list[i])

