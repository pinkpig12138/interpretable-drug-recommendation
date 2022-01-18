from utils import *

#=============================================================================================================
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


#=============================================================================================================
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


# 获取原子_0的关系
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/cui_atom_0.csv", 'r'))
# csv_writer = csv.writer(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/atom_related_atom_0.csv", 'a+', newline=''))
# count = 0
# atom_uri_list = []
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         # csv_writer.writerow(['atom_uri', 'relation', 'related_atom_uri','related_atom_name'])
#         continue
#     atom_uri = line[1]
#     atom_uri_list.append(atom_uri)
# length = len(atom_uri_list)
# print(length)
#多线程
import time
import threading
import inspect
import csv

# 患者特征与CUI的映射





def multi_thread(list, function,seperate_num):
    length = len(list)
    begin = 0
    end = seperate_num
    while end < length:
        current_list = list[begin:end]
        t1 = time.time()
        for i, atom_uri in enumerate(current_list):
            globals()['thread' + str(i)] = threading.Thread(target=function, args=(atom_uri,))
            # print('thread' + str(i), atom_uri, flush=True)
        for i in range(len(current_list)):
            globals()['thread'+str(i)].start()
        for i in range(len(current_list)):
            globals()['thread' + str(i)].join()
        print(begin, end, time.time() - t1,flush=True)
        begin += seperate_num
        end += seperate_num


    current_list = list[begin:]
    t1 = time.time()
    for i, atom_uri in enumerate(current_list):
        globals()['thread' + str(i)] = threading.Thread(target=function, args=(atom_uri,))
    for i in range(len(current_list)):
        globals()['thread'+str(i)].start()
    for i in range(len(current_list)):
        globals()['thread' + str(i)].join()
    f.flush()
    print(begin, length, time.time() - t1,flush=True)



#
#
# ===============================================================================================================================
# 获取所有药物实体的原子信息
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/药物实体链接-1.csv", 'r'))
# f = open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/cui_atom_0.csv", 'w', newline='')
# csv_writer = csv.writer(f)
# count = 0
# cui_list = []
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         csv_writer.writerow(['cui_uri', 'atom_uri'])
#         continue
#     cui_uri = line[2]
#     cui_list.append(cui_uri)
# def write_cui_atom(cui_uri):
#     atom_list = get_atoms_from_a_cui_uri(cui_uri)
#     for atom in atom_list:
#         csv_writer.writerow([cui_uri, atom])
# multi_thread(cui_list, write_cui_atom, 5000)


#
# ===============================================================================================================================
# 获取所有特征实体的原子信息
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/cui_0.csv", 'r'))
# f = open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/cui_atom_0.csv", 'a+', newline='')
# csv_writer = csv.writer(f)
# count = 0
# cui_list = []
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         # csv_writer.writerow(['cui_uri', 'atom_uri'])
#         continue
#     cui_uri = line[0]
#     cui_list.append(cui_uri)
# def write_cui_atom(cui_uri):
#     try:
#         atom_list = get_atoms_from_a_cui_uri(cui_uri)
#     except:
#         print(cui_uri,flush=True)
#         return
#     for atom in atom_list:
#         csv_writer.writerow([cui_uri, atom])
# multi_thread(cui_list, write_cui_atom, 5000)





# 关系为空的写入，报错的不写入
# def write_relations(atom_uri):
#     try:
#         relation_list = get_atom_relations(atom_uri)
#         if not relation_list:
#             csv_writer.writerow([atom_uri])
#         for relation in relation_list:
#             csv_writer.writerow([atom_uri] + relation)
#     except:
#         return

# # 多线程function
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/cui_atom_0.csv", 'r'))
# f = open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/atom_related_atom_0.csv", 'w', newline='')
# csv_writer = csv.writer(f)
# count = 0
# atom_uri_list = []
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         # csv_writer.writerow(['atom_uri', 'relation', 'related_atom_uri','related_atom_name'])
#         continue
#     atom_uri = line[1]
#     atom_uri_list.append(atom_uri)
# atom_uri_list = list(set(atom_uri_list))
# length = len(atom_uri_list)
# print(length)
# multi_thread(atom_uri_list, write_relations, 5000)


# ===============================================================================================================================
# 关系检索康复机制，没有找到关系的原子仅写入原子名称
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/atom_related_atom_0.csv", 'r'))
# f = open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/atom_related_atom_0.csv", 'a+', newline='')
# csv_writer = csv.writer(f)
# count = 0
# complete_atom_uri_list = []
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         continue
#     complete_atom_uri_list.append(line[0])
# complete_atom_uri_list = list(set(complete_atom_uri_list))
# # print(complete_atom_uri_list)
# print(len(complete_atom_uri_list),flush=True)
# for i in complete_atom_uri_list:
#     atom_uri_list.remove(i)
# print(len(atom_uri_list),flush=True)
# print(atom_uri_list,flush=True)
# length = len(atom_uri_list)
# # print(atom_uri_list)
# multi_thread(atom_uri_list, write_relations, 5000)



# ===============================================================================================================================
# 获取原子对应的cui,没有找到cui的原子不写入。
# def write_atom_code_2_cui(atom_code):
#     try:
#         cui_uri = get_atom_code_2_cui(atom_code)
#         if not cui_uri:
#             # csv_writer.writerow(['', atom_code])
#             return
#         else:
#             csv_writer.writerow([cui_uri, atom_code])
#     except:
#         return
# #
# #
# # f = open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/related_cui_atom_0.csv", 'w', newline='')
# # csv_writer = csv.writer(f)
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/atom_related_atom_0.csv", 'r'))
# count = 0
# related_atom_list = []
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         # csv_writer.writerow(['related_cui_uri', 'related_atom_uri'])
#         continue
#     try:
#         related_atom = line[2]
#         related_atom_list.append(related_atom)
#     except:
#         continue
# related_atom_list = list(set(related_atom_list))
# print(len(related_atom_list), '检索到的原子数量',  flush=True)
# # multi_thread(related_atom_list, write_atom_code_2_cui, 5000)
#
#
# # ===============================================================================================================================
# # atom对应cui康复机制，没有找到cui的原子不写入。
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/related_cui_atom_0.csv", 'r'))
# f = open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/related_cui_atom_0.csv", 'a+', newline='')
# csv_writer = csv.writer(f)
# count = 0
# complete_atom_uri_list = []
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         continue
#     complete_atom_uri_list.append(line[1])
# complete_atom_uri_list = list(set(complete_atom_uri_list))
# print(len(complete_atom_uri_list), ' 已对应到cui的原子数量',flush=True)
# for i in complete_atom_uri_list:
#     related_atom_list.remove(i)
# print(len(related_atom_list),' 仍未对应到cui的原子数量', flush=True)
# length = len(related_atom_list)
# multi_thread(related_atom_list, write_atom_code_2_cui, 5000)
#
#


# ===============================================================================================================================
# 获取所有不重复的三元组
#
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/related_cui_atom_0.csv", 'r'))
# f = open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/cui_relation_cui_0.csv", 'w', newline='')
# csv_writer = csv.writer(f)
# count = 0
#
# atom2cui = {}
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         continue
#     cui = line[0]
#     atom = line[1]
#     atom2cui[atom] = cui
# print(len(atom2cui))
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/cui_atom_0.csv", 'r'))
# count = 0
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         continue
#     cui = line[0]
#     atom = line[1]
#     atom2cui[atom] = cui
# print(len(atom2cui))
#
# csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/atom_related_atom_0.csv", 'r'))
# triple_list = []
# count = 0
# for line in csv_reader:
#     if count == 0:
#         count += 1
#         continue
#     try:
#         cui1 = atom2cui[line[0]]
#         relation = line[1]
#         cui2 = atom2cui[line[2]]
#         if cui1 == cui2:
#             count += 1
#             continue
#         triple = [cui1, relation, cui2]
#         if triple in triple_list:
#             continue
#         triple_list.append(triple)
#     except:
#         continue
#
# csv_writer.writerow(['cui_uri', 'relation','cui_uri'])
# print("三元组数量为： ", len(triple_list))
# csv_writer.writerows(triple_list)
# print(count)



# ===============================================================================================================================
# 获取第一层的实体列表和关系列表

# 获取所有cui的信息
def write_cui_information(cui_uri):
    try:
        name, semantic_type = get_cui_information(cui_uri)
    except:
        print(cui_uri)
        return
    csv_writer.writerow([cui_uri,name, semantic_type])
#
#
csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/cui_relation_cui_0.csv", 'r'))
# f = open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/cuis_1.csv", 'w', newline='')
# csv_writer = csv.writer(f)
# f2 = open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/relations_0.csv", 'w', newline='')
# csv_writer2 = csv.writer(f2)

cui_list = []
relation_list = []
count = 0
for line in csv_reader:
    if count == 0:
        count += 1
        # csv_writer.writerow(['cui_uri', 'name', 'semantic_type'])
        # csv_writer2.writerow(['relation'])
        continue
    cui1 = line[0]
    relation = line[1]
    cui2 = line[2]
    cui_list.append(cui1)
    cui_list.append(cui2)
    relation_list.append(relation)
cui_list = list(set(cui_list))
relation_list = list(set(relation_list))
print(len(cui_list))
# print(len(relation_list))

# for relation in relation_list:
#     csv_writer2.writerow([relation])
# f2.flush()

# multi_thread(cui_list, write_cui_information, 5000)


# ===============================================================================================================================
# cui查询康复机制
csv_reader = csv.reader(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/cuis_1.csv", 'r'))
f = open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph/cuis_1.csv", 'a+', newline='')
csv_writer = csv.writer(f)
count = 0
complete_cui_uri_list = []
for line in csv_reader:
    if count == 0:
        count += 1
        continue
    complete_cui_uri_list.append(line[0])
complete_cui_uri_list = list(set(complete_cui_uri_list))
print(len(complete_cui_uri_list),flush=True)
for i in complete_cui_uri_list:
    cui_list.remove(i)
print(len(cui_list),flush=True)
length = len(cui_list)
multi_thread(cui_list, write_cui_information, 5000)



# ===============================================================================================================================
#ndc映射到rxnorm，然后与mimic链接
# ndc2rxnorm_file = "/code/pinkpig/KDD_TX/KDD/构建图谱/data/ndc2rxnorm_mapping.txt"
# import json
# f = open(ndc2rxnorm_file,"r",encoding="utf-8")
# lines = ''
# for line in f:
#     lines = line.replace('\'', '').replace('{','').replace('}','').replace(',','\n').replace('u','')
#     # print(lines)
#     break
# ndc2rxnorm = {}
# for line in lines.split('\n'):
#     ndc = line.split(':')[0].strip()
#     rxnorm = line.split(':')[1].strip()
#     ndc2rxnorm[ndc] = rxnorm
# # print(len(ndc2rxnorm))
# f.close()
# ndc_list = ['00713016550', '00904770418', '00904404073', '00904526161', '63739008901', '00121054410', '00338011704', '00338001702', '00338004938', '00074148402', '10019016312', '00338070341', '00338355248', '00002821501', '00074125901', '00310030011', '51079025520', '55390007310', '66689036430', '00074176230', '51079000220', '00406051262', '00517260225', '00456066270', '00054829725', '58177000111', '00409610204', '00517391025', '51079087101', '00338004903', '66553000401', '00045152010', '00338055002', '00517571025', '00087057007', '00338001704', '00338001731', '00641040025', '63653117103', '51079000522', '00071015823', '67618030011', '00008092355', '00056017675', '55390005710', '00264751020', '00409792337', '00338070541', '51079080120', '00008084199', '00088222033', '00056017075', '00024540134', '00338004902', '00310013039', '00006494300', '00338055318', '00310032520', '00548590000', '00006004368', '63739002401', '51079012620', '00703115303', '64253033335', '00002735501', '00338004904', '00009514001', '00074131230', '00338008504', '66591018442', '00074781124', '00338004931', '00045025501', '00409198530', '00310027539', '00182844789', '00172376010', '51079045620', '51079045120', '00904224461', '00536338101', '00574705050', '00904516561', '00517090125', '60258000601', '61553008348', '00409672924', '00045006601', '58177020211', '63323026201', '51079055271', '00071015640', '00071015540', '00517570425', '00409148402', '00409662502', '17714001110', '61553011841', '00338004304', '54569523500', '00781305714', '00006473900', '00056016975', '00406717162', '51079090620', '51079007220', '00172375810', '10019003783', '10019002710', '00300154430', '17270072101', '00472500360', '52959067430', '51079004120', '60505251903', '00597001314', '00172531210', '00406051201', '51079041720', '00121174410', '00409490234', '00054829925', '00409125830', '00409176230', '00703450204', '00487980125', '00487950125', '00074233411', '00182050789', '49502069724', '00093521193', '00409779362', '00409131230', '10019003867', '00597008717', '59310057920', '10019002804', '00338500241', '00409729501', '00056017275', '00406055262', '51079096620', '00054848616', '51079038620', '00121065721', '00074662502', '51079069020', '00074198530', '00641037625', '00173044202', '11098003002', '00677178110', '00008092303', '00310032130', '17714002001', '00054865724', '00009338901', '00006353750', '00074729501', '63323031461', '00045152510', '00045006801', '50242004413', '00173024256', '00009090020', '17314931102', '00074665305', '51079074520', '51079010320', '00023050601', '00338008904', '00054872425', '00121043130', '00034120081', '00338001703', '00088120806', '58468002101', '00165002241', '00641049125', '49502068524', '00045006701', '10019051002', '60505068104', '51079028520', '55390034810', '00904777261', '00256015201', '00904399061', '08290036005', '00054001820', '00071015723', '00409665305', '10019002803', '00182402889', '00300304613', '00172439018', '63481068706', '00206845525', '63323016501', '00074177825', '00074407532', '62584078833', '00045050130', '00074176201', '00069153041', '58177032304', '63323026920', '63323026965', '63323054011', '68084006501', '54162055007', '00904272561', '51079020520', '00186109239', '00172438210', '00054839224', '00409128331', '63323061401', '00074241612', '00206885216', '00904107061', '00904150061', '00338001701', '55390013020', '46287000660', '00182845389', '00182853489', '00409781124', '63323031110', '00409915801', '25010040515', '51991045757', '00074792201', '00338519741', '51079007320', '00182117089', '00409433201', '00004026001', '00054872625', '10432017002', '00074610204', '63323022110', '00054001720', '00009019016', '00904504561', '00206885516', '00338001710', '55390046001', '00074779362', '58177000104', '49502069703', '00074915801', '00944049101', '00338067104', '00517760425', '60505260400', '00338105102', '00548301200', '00173069602', '00409477702', '63323061603', '67467064301', '00409665106', '51079000620', '51079001920', '00002751001', '00054465025', '00008418806', '51079033530', '00002831501', '10019001303', '55499120401', '63323018410', '00003045051', '00338069104', '63323001302', '00002445385', '00469060773', '00469065773', '55390000401', '00781345295', '00338070948', '00064065001', '10019017644', '00904198861', '00469061711', '00004003822', '55390014710', '63323047401', '51079045420', '00182116189', '00245004101', '00143987310', '00206886202', '00904053061', '00409739172', '63739027201', '00078024615', '00078024815', '43825010201']
# f = open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/药物实体链接-1.csv", 'w', newline='')
# csv_writer = csv.writer(f)
# csv_writer.writerow(['ndc','rxnorm', 'cui_uri'])
#
# # 没查到不写
# def write_ndc_rxnorm_cui(ndc):
#     rxnorm_code = ndc2rxnorm[ndc]
#     atom_uri = 'https://uts-ws.nlm.nih.gov/rest/content/2020AB/source/RXNORM/' + rxnorm_code
#     try:
#         cui_uri = get_atom_code_2_cui(atom_uri)
#         if not cui_uri:
#             # csv_writer.writerow(['', atom_code])
#             return
#         else:
#             csv_writer.writerow([ndc, rxnorm_code, cui_uri])
#     except:
#         return
# multi_thread(ndc_list, write_ndc_rxnorm_cui, 5000)
