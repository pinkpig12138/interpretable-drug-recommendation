import csv
csv_reader = csv.reader(open(r'C:\Users\pinkpigma\pinkpigma的同步盘\KDD研二上\可解释性框架-工作\数据\patient_diagnoses2000_ndc300_with_history.csv', 'r'))
count = 0


for line in csv_reader:
    if count == 0:
        count += 1
        continue
    history_drugs = line[-1].split(';')
    second_drugs = line[-2].split(';')
    first_drugs = line[-3].split(';')
