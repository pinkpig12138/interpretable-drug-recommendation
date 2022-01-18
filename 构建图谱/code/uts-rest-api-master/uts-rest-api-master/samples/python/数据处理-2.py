from utils import *

# 获取所有疾病的链接
# get_concept_from_string('acetaminophen')
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/top2000_disease_icd_name.csv", 'r'))
# csv_writer = csv.writer(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/疾病实体链接-1.csv", 'w', newline=''))
# count = 0
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         csv_writer.writerow(['icd9_code','icd9_long_title', 'umls_name', 'cui', 'rootSource','uri'])
#         continue
#     icd9_long_title = line[2]
#     icd9_code = line[0]
#     result = get_concept_from_string(icd9_long_title)
#     if result:
#         csv_writer.writerow([icd9_code, icd9_long_title, result['name'], result['ui'], result['rootSource'],result['uri']])
#     else:
#         csv_writer.writerow([icd9_code, icd9_long_title])

# 获取所有疾病实体的原子信息
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/疾病实体链接-1.csv", 'r'))
# csv_writer = csv.writer(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/疾病实体对应的原子.csv", 'w', newline=''))
# count = 0
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         csv_writer.writerow(['cui_uri', 'atom_uri'])
#         continue
#     cui_uri = line[5]
#     # print(cui_uri)
#     atom_list = get_atoms_from_a_cui_uri(cui_uri)
#     for atom in atom_list:
#         # print(atom)
#         csv_writer.writerow([cui_uri, atom])

#维护一个原子列表 原子_0 原子_1 层数 1包含0所有的 cui_uri atom_uri  原子无重复
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/疾病实体对应的原子.csv", 'r'))
# csv_writer = csv.writer(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/原子_0.csv", 'w', newline=''))
# count = 0
# atom2cui = {}
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         csv_writer.writerow(['cui_uri', 'atom_uri'])
#         continue
#     cui_uri = line[0]
#     atom_uri = line[1]
#     atom2cui[atom_uri] = cui_uri
# for atom_uri in atom2cui.keys():
#     csv_writer.writerow([atom2cui[atom_uri], atom_uri])


# atom_uri_list = """https://uts-ws.nlm.nih.gov/rest/content/2020AB/source/CPM/65260""".split('\n')
# for arom_uri in atom_uri_list:
#     relation_list = get_atom_relations(arom_uri)
#     print("===================")
#     for relation in relation_list:
#         print(relation)

#
# relation_list = get_atom_relations('https://uts-ws.nlm.nih.gov/rest/content/2020AB/source/RXNORM/161')
# print("===================")
# for relation in relation_list:
#     print(relation)



# 获取原子_0的关系
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/原子_0.csv", 'r'))
# csv_writer = csv.writer(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/原子_0_关系.csv", 'w+', newline=''))
# count = 0
# atom_uri_list = []
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         csv_writer.writerow(['atom_uri', 'relation', 'related_atom_uri','related_atom_name'])
#         continue
#     atom_uri = line[1]
#     atom_uri_list.append(atom_uri)
# length = len(atom_uri_list)
# print(length)

# import time
# t1 = time.time()
# cui_uri = get_atom_code_2_cui('https://uts-ws.nlm.nih.gov/rest/content/2020AB/source/SNOMEDCT_US/192377000')
# print(cui_uri)
# print(time.time()-t1)


import time
t1 = time.time()
atom = get_atoms_from_a_cui_uri('https://uts-ws.nlm.nih.gov/rest/content/2021AB/CUI/C1744601')
print(atom)
print(time.time()-t1)

