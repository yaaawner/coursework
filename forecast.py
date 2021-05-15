import math

MAXK = 10

#TODO: array mae

def drift_moving_average(rate_list, step, k, rtt, cwnd):
    h = (2 + math.log(cwnd, 2)) * rtt
    res = 0
    for i in range(1, k+1):
        res += h * (rate_list[0] - rate_list[i]) / (step * i * k)
    return res

def learning(rate_list, step, k, rtt, cwnd, nowrate):
    h = (2 + math.log(cwnd, 2)) * rtt
    average = 0
    kmin = 1
    min = 100

    if step > h:
        t = 1
    else:
        t = h // step

    for i in range (1, MAXK + 1):
        average += h * (rate_list[t] - rate_list[t + i]) / (step * i)
        res = rate_list[t] + average / i

        if nowrate > res:
            mae = nowrate - res
        else:
            mae = res - nowrate

        if i == 1:
            min = mae
        elif mae < min:
            min = mae
            kmin = i

    return kmin



