from forecast import drift_moving_average
from forecast import learning
import math
import csv

ALPHA = 100
#TODO: io with files

#buf_rate = [55000, 50000, 49000, 46789, 26789, 10920, 20000, 30000, 20000, 40000] #input from file
rtt = 100
cwnd = 100
step = 100
requirement = 10000
buffer = []

time = 0
open_subflow_flag = False

difrate = 0
difstep = 0
index_inc_rate = 0
k = 1
number_flow = 1
subflows = [0]
i = 0
input_file = open('datasets/LTE_Dataset/Dataset/static/A_2017.11.22_10.06.58.csv', 'r')
output_file = open('results/cwnd_pred.csv', 'w', newline='')
reader = csv.DictReader(input_file)
writer = csv.writer(output_file)
#writer.writerow(['Time', 'Rate'])

for row in reader:
    rate = int(row['DL_bitrate'])

    cwnd = rate // rtt + 1
    time += step
    time_to_open_subflow = (2 + math.log(cwnd, 2)) * rtt

    if time_to_open_subflow < step:
        pred = 1
    else:
        pred = time_to_open_subflow // step
    #forecast_list[i + pred] = drift_moving_average(buf_rate, step, k, rtt, cwnd)

    for i in range(len(subflows)):
        subflows[i] = rate

    if open_subflow_flag:
        subflows[-1] = difstep * index_inc_rate
        index_inc_rate += 1

    sumrate = sum(subflows)

    buffer.append(sumrate)
    prediction = drift_moving_average(buffer, step, k, rtt, cwnd)

    if prediction + ALPHA < requirement:
        difrate = rate
        difstep = difrate // pred
        open_subflow_flag = True
        index_inc_rate = 1
        number_flow += 1
        subflows.append(0)

    elif sumrate + ALPHA < requirement:
        k = learning(buffer, step, k, rtt, cwnd, sumrate)
        difrate = rate
        difstep = difrate // pred
        open_subflow_flag = True
        index_inc_rate = 1
        number_flow += 1
        subflows.append(0)

    if sumrate > requirement:
        open_subflow_flag = False
        if number_flow > 1:
            number_flow -= 1
            subflows.pop()

    writer.writerow([str(int(sumrate))])