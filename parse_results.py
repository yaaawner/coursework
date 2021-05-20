import csv

from experiment import rtt_list
from experiment import step_list
from experiment import requirement_list

for step in step_list:
    with open('parse/resultmew_step{}_req_rtt100.csv'.format(step), 'w', newline='') as result_file:
        writer = csv.writer(result_file)
        writer.writerow(['req', 'rtt', 'index_dataset', 'original_avg', 'forecast_avg',
                         'original_percent', 'forecast_percent'])

        for req in requirement_list:
            for rtt in rtt_list:
                orig_avg = []
                fore_avg = []
                orig_perc = []
                fore_perc = []

                for indexdataset in range(1, 2):
                    original_percent = 0
                    forecast_percent = 0
                    original_rate = []
                    forecast_rate = []

                    with open('results_mew/step{}_rtt{}_req{}_data{}.csv'.format(step, rtt, req, indexdataset), 'r') as exp_file:
                        reader = csv.DictReader(exp_file)
                        for row in reader:
                            if int(row['original']) < req:
                                original_percent += 1
                            if int(row['forecast']) < req:
                                forecast_percent += 1
                            original_rate.append(int(row['original']))
                            forecast_rate.append(int(row['forecast']))

                    original_percent //= 5
                    forecast_percent //= 5
                    original_avg = sum(original_rate) // 500
                    forecast_avg = sum(forecast_rate) // 500

                    orig_perc.append(original_percent)
                    orig_avg.append(original_avg)
                    fore_perc.append(forecast_percent)
                    fore_avg.append(forecast_avg)

                writer.writerow([str(req), str(rtt), str(indexdataset),
                                 str(sum(orig_avg)), str(sum(fore_avg)),
                                 str(sum(orig_perc)), str(sum(fore_perc))])



