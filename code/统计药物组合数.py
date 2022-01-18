import csv
csv_reader = csv.reader(open(r'C:\Users\pinkpigma\pinkpigma的同步盘\KDD研二上\可解释性框架-工作\数据\patient_diagnoses2000_ndc300_with_history_delete2.csv', 'r'))

count = 0
com_list = []
for line in csv_reader:
    if count == 0:
        count += 1
        # print(line[5+72+2000+300:5+72+2000+600])
        continue
    new_str = ''
    for i in line[5+72+2000+300:5+72+2000+300+50]:
        new_str += i
    # print(new_str)
    if new_str not in com_list:
        com_list.append(new_str)
    count += 1
print(len(com_list))
print(count - 1)