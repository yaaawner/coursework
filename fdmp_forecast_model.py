from forecast import drift_moving_average
from forecast import learning
import math
import csv

def fdmp_forecast_model(path_to_input_file, path_to_output_file, rtt = 100, requirement = 10000, step = 100):
    ALPHA = 100
    header_csv = ['flow1', 'flow2', 'flow2']
    buffer = []

    time = 0
    open_subflow_flag = False

    difrate = 0
    difstep = 0
    index_inc_rate = 0
    k = 3
    number_flow = 1
    subflows = [0]

    input_file = open(path_to_input_file, 'r')
    #output_file = open(path_to_output_file, 'w', newline='')
    reader = csv.DictReader(input_file)
    #writer = csv.writer(output_file)
#writer.writerow(['Time', 'Rate'])

    counter = 0

    for row in reader:
        counter += 1
        rate = int(row['flow1'])
        cwnd = rate * rtt // 1000 + 1

        time += step
        time_to_open_subflow = (2 + math.log(cwnd, 2)) * rtt

        if time_to_open_subflow < step:
            pred = 1
        else:
            pred = time_to_open_subflow // step
    #forecast_list[i + pred] = drift_moving_average(buf_rate, step, k, rtt, cwnd)

        for i in range(len(subflows)):
            subflows[i] = int(row[header_csv[i % 3]])

        if open_subflow_flag:
            subflows[-1] = int(row[header_csv[len(subflows) % 3]]) // pred * index_inc_rate
            #if subflows[-1]
            index_inc_rate += 1
            if subflows[-1] >= int(row[header_csv[len(subflows) % 3]]):
                open_subflow_flag = False
                #index_inc_rate = 1

        sumrate = sum(subflows)

        buffer.append(sumrate)
        prediction = drift_moving_average(buffer, step, k, rtt, cwnd)

        if prediction + ALPHA < requirement and counter > 10:
            #difrate = rate
            #difstep = difrate // pred
            open_subflow_flag = True
            index_inc_rate = 1
            number_flow += 1
            subflows.append(0)

        elif sumrate + ALPHA < requirement and counter > 10:
            k = learning(buffer, step, k, rtt, cwnd, sumrate)
            #difrate = rate
            #difstep = difrate // pred
            open_subflow_flag = True
            index_inc_rate = 1
            number_flow += 1
            subflows.append(0)

        if sumrate > requirement:
            open_subflow_flag = False
            if number_flow > 1 and sum(subflows[0:-1]) > requirement:
                number_flow -= 1
                subflows.pop()

        #writer.writerow([str(int(sumrate))])
        if int(sum(subflows)) % 10 == 0:
            yield str(int(sum(subflows)) + 111)
        else:
            yield str(int(sum(subflows)))