import csv

csv_reader = csv.reader(open(r'C:\Users\pinkpigma\pinkpigma的同步盘\KDD研二上\可解释性框架-工作\数据\patient_diagnoses2000_ndc300_with_history.csv', 'r'))
count = 0
first_drugs_count = 0
second_drugs_count = 0
history_drugs_count = 0
first_dict = {}
second_dict = {}
for line in csv_reader:
    if count == 0:
        count += 1
        continue

    history_drugs = line[-1].split(';')
    second_drugs = line[-2].split(';')
    first_drugs = line[-3].split(';')

    if first_drugs[0] != '':
        try:
            first_dict[len(first_drugs)] += 1
        except:
            first_dict[len(first_drugs)] = 1
        first_drugs_count += len(first_drugs)
    else:
        try:
            first_dict[0] += 1
        except:
            first_dict[0] = 1
    if second_drugs[0] != '':
        second_drugs_count += len(second_drugs)
        try:
            second_dict[len(first_drugs)] += 1
        except:
            second_dict[len(first_drugs)] = 1
    else:
        try:
            second_dict[0] += 1
        except:
            second_dict[0] = 1
    if history_drugs[0] != '':
        history_drugs_count += len(history_drugs)
    count += 1
count -= 1
print("入院数： ", count)
print("第一天平均用药数： ", first_drugs_count/count)
print("第二天平均用药数： ", second_drugs_count/count)
print("历史平均用药数： ", history_drugs_count/count)

for key in second_dict.keys():
    print(key,'\t', second_dict[key])