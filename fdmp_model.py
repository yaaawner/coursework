import math
import csv

ALPHA = 100
#TODO: io with files

buf_rate = [] #input from file
rtt = 100
cwnd = 100
step = 100
requirement = 10000
time = 0
open_subflow_flag = False
difrate = 0
difstep = 0
index_inc_rate = 0
i = 0

number_flow = 1
subflows = [0]

input_file = open('datasets/LTE_Dataset/Dataset/static/A_2017.11.22_10.06.58.csv', 'r')
output_file = open('results/cwnd_10000.csv', 'w', newline='')
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

    for i in range(len(subflows)):
        subflows[i] = rate

    if open_subflow_flag and len(subflows) > 1:
        subflows[-1] = difstep * index_inc_rate
        index_inc_rate += 1

    if sum(subflows) + ALPHA < requirement:
        difrate = rate
        difstep = difrate // pred
        open_subflow_flag = True
        index_inc_rate = 1
        number_flow += 1
        subflows.append(0)

    if sum(subflows) > requirement:
        open_subflow_flag = False
        if number_flow > 1:
            number_flow -= 1
            subflows.pop()

    #print(time, sum(subflows), rate, number_flow)
    writer.writerow([str(int(sum(subflows)))])