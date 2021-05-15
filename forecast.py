import math

MAXK = 10

#TODO: array mae

def drift_moving_average(rate_list, step, k, rtt, cwnd):
    if len(rate_list) < k+1:
        return rate_list[0]
    h = (2 + math.log(cwnd, 2)) * rtt
    res = 0
    for i in range(1, k+1):
        res += h * (rate_list[-1] - rate_list[-1 - i]) / (step * i * k)
    return res

def learning(rate_list, step, k, rtt, cwnd, nowrate):
    h = (2 + math.log(cwnd, 2)) * rtt
    average = 0
    kmin = 1
    min = 100

    if step > h:
        t = 1
    else:
        t = int(h // step)

    #if t > len(rate_list):
        #t = len(rate)

    if MAXK > len(rate_list):
        maxk = len(rate_list) -1
    else:
        maxk = MAXK

    if len(rate_list) < t + maxk:
        maxk = len(rate_list) - t - 1

    for i in range (1, maxk):
        average += h * (rate_list[-1 - t] - rate_list[-1 -t - i]) / (step * i)
        res = rate_list[-1 - t] + average / i

        mae = nowrate - res

        if i == 1:
            min = mae
        elif mae < min:
            min = mae
            kmin = i

    return kmin



