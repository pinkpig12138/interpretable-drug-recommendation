#coding=utf-8
from Authentication import *
import requests
import json
import all_path, csv
from tqdm import tqdm
import sys
import io
import time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf8")  ## encoding 的参数写成网站的编码格式即可


csv_writer = csv.writer(open(all_path.kg_file, "a+", encoding="utf-8", newline=''))
apikey = "bb6e7f92-bf27-48df-99a1-369cbac50f7f"
version = "2020AB"
source = None
AuthClient = Authentication(apikey)

tgt = AuthClient.gettgt()
uri = "https://uts-ws.nlm.nih.gov"
ticket = AuthClient.getst(tgt)

def get_atom_code_2_cui(atom_code):
    # print(atom_code)
    cui_uri = ''
    query = {'ticket':AuthClient.getst(tgt), 'pageNumber':1}
    if 'AUI' in atom_code:
        r = requests.get(atom_code, params=query)
        r.encoding = 'utf-8'
        items = json.loads(r.text)
        try:
            cui_uri = items['result']['concept']
        except:
            print(atom_code)
    else:
        r = requests.get(atom_code + "/atoms",params=query)
        r.encoding = 'utf-8'
        items  = json.loads(r.text)
        try:
            cui_uri = items['result'][0]['concept']
        except:
            print(atom_code)

    return cui_uri

def get_atom_code_relations(atom_code):
    pageNumber = 1
    relation_list = []

    while True:
        query = {'ticket': AuthClient.getst(tgt), 'pageNumber': pageNumber}
        r = requests.get(atom_code + "/relations", params=query)
        # r = requests.get("https://uts-ws.nlm.nih.gov/rest/content/2020AB/CUI/C0002645/atoms", params=query)
        r.encoding = 'utf-8'
        items = json.loads(r.text)
        # print(items)
        try:
            pageCount = items['pageCount']
        except:
            break

        if pageCount == 0:
            break
        for item in items['result']:
            # print(item)
            relation_list.append(list(item.values()))

        pageNumber += 1
        if pageNumber > pageCount:
            break
    return relation_list

def get_cui_atom_relations(cui):
    ##generate a new service ticket for each page if needed

    pageNumber = 1
    pageCount = 0

    atom_code_list = []
    while True:
        query = {'ticket':AuthClient.getst(tgt), 'pageNumber':pageNumber}
        # r = requests.get("https://uts-ws.nlm.nih.gov/rest/content/current/source/MTH/NOCODE/relations",params=query)
        r = requests.get("https://uts-ws.nlm.nih.gov/rest/content/2020AB/CUI/" + cui + "/atoms", params=query)
        r.encoding = 'utf-8'
        atom_items  = json.loads(r.text)
        # print(atom_items)
        try:
            pageCount = atom_items['pageCount']
        except:
            break

        for atom in atom_items['result']:
            atom_code_list.append(atom['code'])

        pageNumber += 1
        if pageNumber>pageCount:
            break
    relation_list = []
    for atom_code in tqdm(atom_code_list):
        # print(atom_code)
        relation_list.extend(get_atom_code_relations(atom_code))
    return relation_list








def get_atom_relation_from_cuis(cui_list, umls_name_list):
    for index in range(len(cui_list)):
        cui = cui_list[index]
        umls_name = umls_name_list[index]

        print(cui, umls_name)
        sys.stdout.flush()
        relation_list = get_cui_atom_relations(cui)
        for relation in relation_list:
            csv_writer.writerow([umls_name, cui] + relation + [get_atom_code_2_cui(relation[-2])])
            # print([umls_name, cui] + relation)


title = ['umls_name', 'cui', 'classType', 'ui', 'suppressible', 'sourceUi', 'obsolete', 'sourceOriginated', 'rootSource', 'relationLabel', 'additionalRelationLabel', 'groupId', 'attributeCount', 'relatedId', 'relatedIdName','relatedCui']
umls_name_list = all_path.umls_name_list
cui_list = all_path.cui_list


umls_name_list = umls_name_list[:10]
cui_list = cui_list[:10]
# csv_writer.writerow(title)
get_atom_relation_from_cuis(cui_list, umls_name_list)




