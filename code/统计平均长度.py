import csv

csv_reader = csv.reader(open("/code/pinkpig/afa/data/feature40_class10_41401.csv", 'r', encoding='gbk'))
classes = [225798,225893,225850,225884,225459,224275,225402,224277,225752,225792]
all_length = 0
current_length = 0
current_icustay_id = 0
sequence_num = 0
for line in csv_reader:
    itemid = int(line[4])
    icustay_id = line[2]
    if icustay_id != current_icustay_id:
        if itemid in classes:
            sequence_num += 1
            all_length += current_length
            current_length = 0
        else:
            current_length = 1
        current_icustay_id = icustay_id
    elif itemid in classes:
        sequence_num += 1
        all_length += current_length
        current_length = 0
    else:
        current_length += 1
print(sequence_num, all_length/sequence_num)