import csv
import pprint
path = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/prototype_result.csv"
def write_csv(path, result,):
    header = ['system_time', 'MEC_num', 'device_num', 'max_hop', 'max_hop_device', 'min_hop', 'min_hop_device',
              'average_hop', 'AP_reboot_rate']
    result_num = len(result)
    #csv_index = [num for num in range(result_num)]
    csv_index = [1]
    print(csv_index)
    #for csv_num in range(result_num):
        #csv_index.appned(csv_num)
    with open(path, mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(result)
        #for i, row in zip(csv_index, result):
           # writer.writerow([i] + row)
