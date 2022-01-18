from utils import *
import time
import threading
import csv

# 定义层数
level = 3

# 从第几层开始
start_level = 1

# 同时运行多少个线程
thread_num = 5000

# 复检最大次数
restart_times = 100


# 生成文件名
cui_file_list = []
cui_atom_file_list = []
atom_related_atom_file_list = []
related_cui_atom_file_list = []
cui_relation_cui_file_list = []


cui_title = ['cui_uri', 'name', 'semantic_type']
cui_atom_title = ['cui_uri', 'atom_uri']
atom_related_atom_title = ['atom_uri', 'relation', 'related_atom_uri','related_atom_name']
related_cui_atom_title = ['related_cui_uri', 'related_atom_uri']
cui_relation_cui_title = ['cui_uri', 'relation','cui_uri']


base_dict = '/code/pinkpig/KDD_TX/KDD/构建图谱/data/graph_now/'
for i in range(level):
    cui_file_list.append(base_dict + 'cuis_' + str(i) + '.csv')
    cui_atom_file_list.append(base_dict + 'cui_atom_' + str(i) + '.csv')
    atom_related_atom_file_list.append(base_dict + 'atom_related_atom_' + str(i) + '.csv')
    related_cui_atom_file_list.append(base_dict + 'related_cui_atom_' + str(i) + '.csv')
    cui_relation_cui_file_list.append(base_dict + 'cui_relation_cui_' + str(i) + '.csv')
# print(cui_file_list)
# print(cui_atom_file_list)
# print(atom_related_atom_file_list)
# print(related_cui_atom_file_list)
# print(cui_relation_cui_file_list)






def construct_graph(current_level, thread_num):
    def multi_thread(list, function, seperate_num):
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
                globals()['thread' + str(i)].start()
            for i in range(len(current_list)):
                globals()['thread' + str(i)].join()
            print(begin, end, time.time() - t1, flush=True)
            begin += seperate_num
            end += seperate_num

        current_list = list[begin:]
        t1 = time.time()
        for i, atom_uri in enumerate(current_list):
            globals()['thread' + str(i)] = threading.Thread(target=function, args=(atom_uri,))
        for i in range(len(current_list)):
            globals()['thread' + str(i)].start()
        for i in range(len(current_list)):
            globals()['thread' + str(i)].join()
        f.flush()
        print(begin, length, time.time() - t1, flush=True)


    print("正在处理的层为： " + str(current_level))
    # retrieved_cui_list = []
    # try:
    #     cui_file = csv.reader(open(cui_file_list[current_level-1], 'r'))
    #     count = 0
    #     for line in cui_file:
    #         if count == 0:
    #             count += 1
    #             continue
    #         cui_uri = line[0]
    #         retrieved_cui_list.append(cui_uri)
    # except:
    #     cui_file = csv_reader = csv.reader(open(cui_file_list[0], 'r'))
    # print("前面的层数中已经检索过的cui数量为： " + str(len(retrieved_cui_list)), flush=True)
    #
    #
    # current_cui_file = csv.reader(open(cui_file_list[current_level], 'r'))
    # current_cui_list = []
    # count = 0
    # for line in current_cui_file:
    #     if count == 0:
    #         count += 1
    #         continue
    #     cui_uri = line[0]
    #     count += 1
    #     if cui_uri not in retrieved_cui_list:
    #         current_cui_list.append(cui_uri)
    # print("这一层共有cui数量为：" + str(count-1), flush=True)
    # print("待检索的cui数量为："+ str(len(current_cui_list)), flush=True)
    #
    # #===================================
    # # 开始检索原子,没有原子的和检索出错的都不写入
    # f = open(cui_atom_file_list[current_level], 'a+', newline='')
    # csv_writer = csv.writer(f)
    # # csv_writer.writerow(cui_atom_title)
    # # 定义函数
    # def write_cui_atom(cui_uri):
    #     try:
    #         atom_list = get_atoms_from_a_cui_uri(cui_uri)
    #     except:
    #         # print(cui_uri + '     未写入', flush=True)
    #         return
    #     for atom in atom_list:
    #         csv_writer.writerow([cui_uri, atom])
    #
    # # 开始检索
    # # multi_thread(current_cui_list, write_cui_atom, thread_num)
    #
    # # 开始复检
    # last_remain_num = len(current_cui_list)
    # for i in range(restart_times):
    #     print("复检次数：", i)
    #     csv_reader = csv.reader(open(cui_atom_file_list[current_level], 'r'))
    #     complete_list = []
    #     count = 0
    #     for line in csv_reader:
    #         if count == 0:
    #             count += 1
    #             continue
    #         complete_list.append(line[0])
    #     complete_list = list(set(complete_list))
    #     print(len(complete_list), ' 已检索好atom的cui数量',flush=True)
    #     for item in complete_list:
    #         try:
    #             current_cui_list.remove(item)
    #         except:
    #             continue
    #     current_remain_num = len(current_cui_list)
    #     print("仍待检索的cui数量为：" + str(current_remain_num), flush=True)
    #     if (current_remain_num == 0) or (current_remain_num == last_remain_num):
    #         break
    #     multi_thread(current_cui_list, write_cui_atom, thread_num)
    #     last_remain_num = current_remain_num
    # f.close()

   #===================================
    # 开始检索原子相关的关系，如果关系为空，单独写入原子名称，如果检索出错不写入
    f = open(atom_related_atom_file_list[current_level], 'a+', newline='')
    csv_writer = csv.writer(f)
    # csv_writer.writerow(atom_related_atom_title)
    # 定义函数
    def write_relations(atom_uri):
        try:
            relation_list = get_atom_relations(atom_uri)
            if not relation_list:
                csv_writer.writerow([atom_uri])
            for relation in relation_list:
                csv_writer.writerow([atom_uri] + relation)
        except:
            return

    csv_reader = csv.reader(open(cui_atom_file_list[current_level], 'r'))
    atom_list = []
    count = 0
    for line in csv_reader:
        if count == 0:
            count += 1
            continue
        atom = line[1]
        if atom not in atom_list:
            atom_list.append(atom)
    # print("待检索关系的原子数量为： ", len(atom_list), flush=True) #不含重复，不含空
    # multi_thread(atom_list, write_relations, thread_num)

    # 开始复检
    last_remain_num = len(atom_list)
    for i in range(restart_times):
        print("复检次数：", i, flush=True)
        csv_reader = csv.reader(open(atom_related_atom_file_list[current_level], 'r'))
        complete_list = []
        count = 0
        for line in csv_reader:
            if count == 0:
                count += 1
                continue
            complete_list.append(line[0])
        complete_list = list(set(complete_list))
        print(len(complete_list), ' 已检索好关系的atom数量', flush=True)
        for item in complete_list:
            try:
                atom_list.remove(item)
            except:
                continue
        current_remain_num = len(atom_list)
        print("仍待检索关系的atom数量为：" + str(current_remain_num), flush=True)
        if (current_remain_num == 0) or (current_remain_num == last_remain_num):
            break
        multi_thread(atom_list, write_relations, thread_num)
        last_remain_num = current_remain_num


    # ===============================================================================================================================
    # 获取原子对应的cui,没有找到cui的原子不写入。
    f.close()
    f = open(related_cui_atom_file_list[current_level], 'w', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(related_cui_atom_title)
    # 定义函数
    def write_atom_code_2_cui(atom_code):
        try:
            cui_uri = get_atom_code_2_cui(atom_code)
            if not cui_uri:
                # csv_writer.writerow(['', atom_code])
                return
            else:
                csv_writer.writerow([cui_uri, atom_code])
        except:
            return

    csv_reader = csv.reader(open(atom_related_atom_file_list[current_level], 'r'))
    count = 0
    related_atom_list = []
    for line in csv_reader:
        if count == 0:
            count += 1
            continue
        try:
            related_atom = line[2]
            related_atom_list.append(related_atom)
        except:
            continue
    related_atom_list = list(set(related_atom_list))
    print(len(related_atom_list), '待检索CUI的相关原子数量',  flush=True)
    multi_thread(related_atom_list, write_atom_code_2_cui, thread_num)

    # 开始复检
    last_remain_num = len(related_atom_list)
    for i in range(restart_times):
        print("复检次数：", i)
        csv_reader = csv.reader(open(related_cui_atom_file_list[current_level], 'r'))
        complete_list = []
        count = 0
        for line in csv_reader:
            if count == 0:
                count += 1
                continue
            complete_list.append(line[1])
        complete_list = list(set(complete_list))
        print(len(complete_list), ' 已检索好CUI的相关atom数量', flush=True)
        for item in complete_list:
            try:
                related_atom_list.remove(item)
            except:
                continue
        current_remain_num = len(related_atom_list)
        print("仍待检索关系的atom数量为：" + str(current_remain_num), flush=True)
        if (current_remain_num == 0) or (current_remain_num == last_remain_num):
            break
        multi_thread(related_atom_list, write_atom_code_2_cui, thread_num)
        last_remain_num = current_remain_num




    # ===============================================================================================================================
    # 获取所有不重复的三元组
    csv_reader = csv.reader(open(related_cui_atom_file_list[current_level], 'r'))
    f = open(cui_relation_cui_file_list[current_level], 'w', newline='')
    csv_writer = csv.writer(f)
    count = 0

    atom2cui = {}
    for line in csv_reader:
        if count == 0:
            count += 1
            continue
        cui = line[0]
        atom = line[1]
        atom2cui[atom] = cui
    print(len(atom2cui))
    csv_reader = csv.reader(open(cui_atom_file_list[current_level], 'r'))
    count = 0
    for line in csv_reader:
        if count == 0:
            count += 1
            continue
        cui = line[0]
        atom = line[1]
        atom2cui[atom] = cui
    print(len(atom2cui))

    csv_reader = csv.reader(open(atom_related_atom_file_list[current_level], 'r'))
    triple_list = []
    count = 0
    for line in csv_reader:
        if count == 0:
            count += 1
            continue
        try:
            cui1 = atom2cui[line[0]]
            relation = line[1]
            cui2 = atom2cui[line[2]]
            if cui1 == cui2:
                continue
            triple = [cui1, relation, cui2]
            if triple in triple_list:
                continue
            triple_list.append(triple)
        except:
            continue

    csv_writer.writerow(cui_relation_cui_title)
    print("三元组数量为： ", len(triple_list))
    csv_writer.writerows(triple_list)

    # ===============================================================================================================================
    # 获取下一层的实体列表
    # 获取所有cui的信息
    def write_cui_information(cui_uri):
        try:
            name, semantic_type = get_cui_information(cui_uri)
            csv_writer.writerow([cui_uri, name, semantic_type])
        except:
            # print(cui_uri)
            return

    f = open(cui_file_list[current_level + 1], 'w', newline='')
    csv_writer = csv.writer(f)

    cui_list = []
    relation_list = []
    csv_reader = csv.reader(open(cui_relation_cui_file_list[current_level], 'r'))
    count = 0
    for line in csv_reader:
        if count == 0:
            count += 1
            csv_writer.writerow(cui_title)
            continue
        cui1 = line[0]
        relation = line[1]
        cui2 = line[2]
        cui_list.append(cui1)
        cui_list.append(cui2)
        relation_list.append(relation)
    cui_list = list(set(cui_list))
    relation_list = list(set(relation_list))
    print('该层检索结束后包含的实体个数：', len(cui_list))
    print('该层检索结束后包含的关系个数：',len(relation_list))

    multi_thread(cui_list, write_cui_information, thread_num)

    # 开始复检
    last_remain_num = len(cui_list)
    for i in range(restart_times):
        print("复检次数：", i)
        csv_reader = csv.reader(open(cui_file_list[current_level + 1], 'r'))
        complete_list = []
        count = 0
        for line in csv_reader:


            if count == 0:
                count += 1
                continue
            complete_list.append(line[0])
        complete_list = list(set(complete_list))
        print(len(complete_list), ' 已检索好信息的CUI数量', flush=True)
        for item in complete_list:
            try:
                related_atom_list.remove(item)
            except:
                continue
        current_remain_num = len(cui_list)
        print("仍待检索信息的CUI数量为：" + str(current_remain_num), flush=True)
        if (current_remain_num == 0) or (current_remain_num == last_remain_num):
            break
        multi_thread(cui_list, write_cui_information, thread_num)
        last_remain_num = current_remain_num

    return

construct_graph(start_level,thread_num)