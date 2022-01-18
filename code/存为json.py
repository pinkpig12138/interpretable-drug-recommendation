import json

import csv

csv_reader = csv.reader(open("F:\PycharmProjects\AFA\data\lab20_class10_41401.csv", 'r'))


classes = [225798,225893,225850,225884,225459,224275,225402,224277,225752,225792]

current_icustay_id = 200007
sequence_num = 0
dict_list = []
new_dict = {}
step = 0
last_time = ''

for line in csv_reader:
    itemid = int(line[4])
    label = line[5]
    current_time = line[3]
    icustay_id = line[2]
    try:
        value = float(line[6])
    except:
        print()


    if icustay_id != current_icustay_id:
        if itemid in classes:
            new_dict['label'] = label
            dict_list.append(new_dict)
        new_dict = {"steps":{}, "label":''}
        step = 0
        current_icustay_id = icustay_id
    else:
        if itemid in classes:
            new_dict['label'] = label
            dict_list.append(new_dict)
            new_dict = {"steps":{}, "label":''}
            step = 0
        else:
            if current_time != last_time:
                last_time = current_time
                step += 1
            try:
                new_dict["steps"][step][label] = value
            except:
                new_dict["steps"][step] = {}
                new_dict["steps"][step][label] = value
print(len(dict_list))


count = 0
total_length = 0
for dict in dict_list:
    if dict["steps"] != {}:
        # print(dict)
        count += 1
        total_length += len(dict["steps"])
print(count,total_length)

import json
import os
def write_list_to_json(dict_list, json_file_name):
    """
    将list写入到json文件
    :param list:
    :param json_file_name: 写入的json文件名字
    :param json_file_save_path: json文件存储路径
    :return:
    """
    with open(json_file_name, 'w') as  f:
        count = 0
        total_length = 0
        for dict in dict_list:
            if dict["steps"] != {}:
                # print(dict)
                count += 1
                total_length += len(dict["steps"])
                f.write(str(dict) + '\n')
        print(count, total_length)

write_list_to_json(dict_list, "F:\PycharmProjects\AFA\data\lab20_class10_41401.json")



