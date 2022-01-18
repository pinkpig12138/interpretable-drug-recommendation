import csv

dict1 = '/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/'
dict2 = '/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph_疾病/'
dict3 = '/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph_now/'

file = 'cui_atom_0.csv'
csv_reader = csv.reader(open(dict1+file, 'r'))

f = open(dict3 + file, 'w', newline='')
csv_writer = csv.writer(f)

count = 0
line_list = []
for line in csv_reader:
    if count == 0:
        count += 1
        csv_writer.writerow(line)
        continue
    line_list.append(line)
print(len(line_list))

csv_reader = csv.reader(open(dict2+file, 'r'))
count = 0
for line in csv_reader:
    if count == 0:
        count += 1
        csv_writer.writerow(line)
        continue
    if line not in line_list:
        line_list.append(line)
print(len(line_list))
csv_writer.writerows(line_list)




