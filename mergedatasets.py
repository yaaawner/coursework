import os
import csv

path_lte = 'datasets/LTE_Dataset/Dataset/static/'
datasets_lte = os.listdir(path_lte)

path_merge_datasets_list = [
    'datasets/merge/test1.csv',
    'datasets/merge/test2.csv',
    'datasets/merge/test3.csv',
    'datasets/merge/test4.csv',
    'datasets/merge/test5.csv',
]

for index_datasets in range(5):
    #merge_file = open(path_merge_datasets_list[index_datasets], 'w', newline='')
    #writer = csv.writer(merge_file)
    #writer.writerow(['flow1', 'flow2', 'flow3'])
    flows = []
    for dataset in datasets_lte[0+index_datasets:3+index_datasets]:
        with open(path_lte + dataset, 'r') as data_file:
            reader = csv.DictReader(data_file)

            flows.append([])
            i = 0
            for row in reader:
                flows[-1].append(row['DL_bitrate'])
                i += 1
                if i == 500:
                    break

    with open(path_merge_datasets_list[index_datasets], 'w', newline='') as merge_file:
        writer = csv.writer(merge_file)
        writer.writerow(['flow1', 'flow2', 'flow3'])
        #writer.writerows(flows)
        for row_index in range(500):
            writer.writerow([flows[0][row_index], flows[1][row_index], flows[2][row_index]])




