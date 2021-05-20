from mergedatasets import path_merge_datasets_list
import random
import csv

count = 10

path_merge_datasets_list_step100 = [
    'datasets/merge/test1_100.csv',
    'datasets/merge/test2_100.csv',
    'datasets/merge/test3_100.csv',
    'datasets/merge/test4_100.csv',
    'datasets/merge/test5_100.csv',
]

for indexdataset in range(5):
    flow1 = []
    flow2 = []
    flow3 = []

    with open(path_merge_datasets_list[indexdataset], 'r') as merge_file:
        reader = csv.DictReader(merge_file)

        flow1_prev = 0
        flow2_prev = 0
        flow3_prev = 0
        flow1_now = 0
        flow2_now = 0
        flow3_now = 0
        c = 0
        for row in reader:
            if c == 0:
                flow1_now = int(row['flow1'])
                flow2_now = int(row['flow2'])
                flow3_now = int(row['flow3'])

                #flow1.append(flow1_now)
                #flow2.append(flow2_now)
                #flow3.append(flow3_now)
            elif c == 101:
                break
            else:
                flow1_prev = flow1_now
                flow2_prev = flow2_now
                flow3_prev = flow3_now
                flow1_now = int(row['flow1'])
                flow2_now = int(row['flow2'])
                flow3_now = int(row['flow3'])

                for i in range(count):
                    if i == 0:
                        inter = flow1_prev
                        flow1.append(inter)
                    else:
                        if flow1_now > flow1_prev:
                            inter = int(random.uniform(inter, flow1_now))
                        else:
                            inter = int(random.uniform(flow1_now, inter))
                        flow1.append(inter)

                for i in range(count):
                    if i == 0:
                        inter = flow2_prev
                        flow2.append(inter)
                    else:
                        if flow2_now > flow2_prev:
                            inter = int(random.uniform(inter, flow2_now))
                        else:
                            inter = int(random.uniform(flow2_now, inter))
                        flow2.append(inter)

                for i in range(count):
                    if i == 0:
                        inter = flow3_prev
                        flow3.append(inter)
                    else:
                        if flow3_now > flow3_prev:
                            inter = int(random.uniform(inter, flow3_now))
                        else:
                            inter = int(random.uniform(flow3_now, inter))
                        flow3.append(inter)
            c += 1

        with open(path_merge_datasets_list_step100[indexdataset], 'w', newline='') as step100_file:
            writer = csv.writer(step100_file)
            writer.writerow(['flow1', 'flow2', 'flow3'])

            for i in range(len(flow1)):
                writer.writerow([str(flow1[i]), str(flow2[i]), str(flow3[i])])