import os
from fdmp_model import fdmp_model
from fdmp_forecast_model import fdmp_forecast_model
from mergedatasets import path_merge_datasets_list
import csv
from interpolation import path_merge_datasets_list_step100

rtt_list = [100]
step_list = [1000, ]
requirement_list = [1000*i for i in range(1, 100)]

#TODO datasets_ns3
#indexdataset = 0

for step in step_list:
    for rtt in rtt_list:
        for req in requirement_list:

            indexdataset = 0
            for dataset in path_merge_datasets_list:
                indexdataset += 1
                with open(dataset, 'r') as f:
                    reader = csv.DictReader(f)

                    original = [str(i) for i in fdmp_model(dataset, 'test/test.csv', rtt, req, step)]
                    forecast = [str(i) for i in fdmp_forecast_model(dataset, 'test/test.csv', rtt, req, step)]

                with open('results_mew/step{}_rtt{}_req{}_data{}.csv'.format(step, rtt, req, indexdataset), 'w', newline='') as result_file:
                    writer = csv.writer(result_file)
                    writer.writerow(['original', 'forecast'])

                    for row_index in range(500):
                        writer.writerow([original[row_index], forecast[row_index]])
