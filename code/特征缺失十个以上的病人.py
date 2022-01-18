import csv
csv_reader = csv.reader(open(r'C:\Users\pinkpigma\pinkpigma的同步盘\KDD研二上\可解释性框架-工作\数据\patient_diagnoses2000_ndc300_with_history.csv', 'r'))
count = 0
delete_list = []
for line in csv_reader:
    if count == 0:
        count += 1
        continue
    patient_features = line[3:-4]
    # print(patient_features)
    if patient_features.count('') > 10:
        delete_list.append(line[1])
print(len(delete_list))
