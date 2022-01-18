#coding=utf-8
from Authentication import *
import requests
import json
import all_path, csv
from tqdm import tqdm
import sys
import io
import time
from sys import argv, stdout as cout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf8")  ## encoding 的参数写成网站的编码格式即可
apikey = "bb6e7f92-bf27-48df-99a1-369cbac50f7f"
version = "2020AB"
source = None
AuthClient = Authentication(apikey)

tgt = AuthClient.gettgt()
uri = "https://uts-ws.nlm.nih.gov"
ticket = AuthClient.getst(tgt)
except_dict = ['MDRBPO','CPTSP', 'DMDICD10', 'ICD10DUT', 'ICPCBAQ', 'ICPCDAN', 'ICPCDUT', 'ICPCFIN', 'ICPCFRE', 'ICPCGER', 'ICPCHEB', 'ICPCHUN', 'ICPCITA', 'ICPCNOR', 'ICPCPOR', 'ICPCSPA', 'ICPCSWE', 'ICPC2ICD10DUT', 'ICPC2EDUT', 'HLREL', 'KCD5', 'LNC-ZH-CN', 'LNC-NL-NL', 'LNC-ET-EE', 'LNC-FR-BE', 'LNC-FR-CA', 'LNC-FR-FR', 'LNC-FR-CH', 'LNC-DE-AT', 'LNC-DE-DE', 'LNC-DE-CH', 'LNC-EL-GR', 'LNC-IT-IT', 'LNC-IT-CH', 'LNC-KO-KR', 'LNC-PT-BR', 'LNC-RU-RU', 'LNC-ES-AR', 'LNC-ES-ES', 'LNC-ES-CH', 'LNC-TR-TR', 'MDRCZE', 'MDRDUT', 'MDRFRE', 'MDRGER', 'MDRHUN', 'MDRITA', 'MDRJPN', 'MDRKOR', 'MDRPOR', 'MDRRUS', 'MDRSPA', 'MSHSCR', 'MSHCZE', 'MSHDUT', 'MSHFIN', 'MSHFRE', 'MSHGER', 'MSHITA', 'MSHJPN', 'MSHLAV', 'MSHNOR', 'MSHPOL', 'MSHPOR', 'MSHRUS', 'MSHSPA', 'MSHSWE', 'MTHMSTFRE', 'MTHMSTITA', 'NCISEER', 'SCTSPA', 'TKMT', 'DMDUMD', 'WHOFRE', 'WHOGER', 'WHOPOR', 'WHOSPA']
except_relation_label = ['SY','SIB'] #SIB是兄弟姐妹
except_relation_additional = ['concept_in_subset','has_tradename', 'same_as', 'mapped_to', 'mapped_from','primary_mapped_to', 'primary_mapped_from', 'default_mapped_to', 'default_mapped_from', 'multiply_mapped_from', 'multiply_mapped_to', 'other_mapped_from', 'other_mapped_to', 'uniquely_mapped_from', 'uniquely_mapped_to', 'subset_includes_concept' ]

def get_concept_from_string(string):
    pageNumber = 0
    content_endpoint = "/rest/search/" + version
    while True:
        ##generate a new service ticket for each page if needed
        ticket = AuthClient.getst(tgt)
        pageNumber += 1
        query = {'string': string, 'ticket': ticket, 'pageNumber': pageNumber}
        r = requests.get(uri + content_endpoint, params=query)
        r.encoding = 'utf-8'
        items = json.loads(r.text)
        # print(items)
        jsonData = items["result"]
        if jsonData["results"][0]["ui"] == "NONE":
            break
        # print (json.dumps(items, indent = 4))
        # print(jsonData)
        for result in jsonData["results"]:
            if result['rootSource'] in except_dict:
                continue
            # print(result)
            cout.flush()
            return result
    return False


def get_concept_from_string_list(string_list):
    result_list = []
    for string in string_list:
        result = get_concept_from_string(string)
        if result:
            result_list.append([string,result['name'], result['ui'], result['rootSource'],result['uri']])
        else:
            result_list.append([string])
    return result_list

def get_relations_from_an_atom(atom_code_uri):
    relation_list = []
    pageNumber = 0
    while True:
        pageNumber += 1
        query = {'ticket': AuthClient.getst(tgt), 'pageNumber': pageNumber}
        r = requests.get(atom_code_uri + "/relations", params=query)
        r.encoding = 'utf-8'
        items = json.loads(r.text)
        # print(items)
        for item in items['result']:
            # print(item)
            relation_list.append(list(item.values()))
    return relation_list

def get_atoms_from_a_cui_uri(cui_uri):
    pageNumber = 0
    atom_code_list = []
    while True:
        pageNumber += 1
        query = {'ticket': AuthClient.getst(tgt), 'pageNumber': pageNumber}
        # r = requests.get("https://uts-ws.nlm.nih.gov/rest/content/current/source/MTH/NOCODE/relations",params=query)
        r = requests.get(cui_uri + "/atoms", params=query)
        r.encoding = 'utf-8'
        atom_items = json.loads(r.text)
        # print(atom_items)
        if not atom_items['result'] :
            break
        # print(atom_items)
        for atom in atom_items['result']:
            atom_code = atom['code']
            if atom_code.split('/')[-2] in except_dict:
                continue
            atom_code_list.append(atom_code)
    return list(set(atom_code_list))

def get_atom_relations(atom_uri):
    pageNumber = 1
    relation_list = []

    while True:
        query = {'ticket': AuthClient.getst(tgt), 'pageNumber': pageNumber}
        r = requests.get(atom_uri + "/relations", params=query)
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
            related_atom_uri = item['relatedId']
            related_atom_name = item['relatedIdName']
            relationLabel = item['relationLabel']
            relation_name = item['additionalRelationLabel']
            if relationLabel in except_relation_label:
                continue
            if relation_name in except_relation_additional:
                continue
            relation_list.append([relationLabel + ':' + relation_name,related_atom_uri, related_atom_name])

        pageNumber += 1
        if pageNumber > pageCount:
            break
    return relation_list

def get_atom_relations(atom_uri):
    pageNumber = 1
    relation_list = []
    tgt = AuthClient.gettgt()
    while True:
        query = {'ticket': AuthClient.getst(tgt), 'pageNumber': pageNumber}
        r = requests.get(atom_uri + "/relations", params=query)
        # r = requests.get("https://uts-ws.nlm.nih.gov/rest/content/2020AB/CUI/C0002645/atoms", params=query)
        r.encoding = 'utf-8'
        items = json.loads(r.text)

        # print(atom_uri)
        # print(items)
        try:
            pageCount = items['pageCount']
        except:
            break

        if pageCount == 0:
            break
        for item in items['result']:
            # print(item)
            related_atom_uri = item['relatedId']
            related_atom_name = item['relatedIdName']
            relationLabel = item['relationLabel']
            relation_name = item['additionalRelationLabel']
            if relationLabel in except_relation_label:
                continue
            if relation_name in except_relation_additional:
                continue
            relation_list.append([relationLabel + ':' + relation_name,related_atom_uri, related_atom_name])

        pageNumber += 1
        if pageNumber > pageCount:
            break
    return relation_list

# 找不到cui的atom
def get_atom_code_2_cui(atom_uri):
    # print(atom_code)
    tgt = AuthClient.gettgt()
    query = {'ticket':AuthClient.getst(tgt), 'pageNumber':1}
    if 'AUI' in atom_uri:
        r = requests.get(atom_uri, params=query)
        r.encoding = 'utf-8'
        items = json.loads(r.text)
        try:
            cui_uri = items['result']['concept']
        except:
            # print(atom_uri)
            return False
    else:
        r = requests.get(atom_uri + "/atoms",params=query)
        r.encoding = 'utf-8'
        items  = json.loads(r.text)
        try:
            cui_uri = items['result'][0]['concept']
        except:
            # print(atom_uri)
            return False
    return cui_uri


# 获取一个cui的所有信息
def get_cui_information(cui_uri):
    tgt = AuthClient.gettgt()
    query = {'ticket': AuthClient.getst(tgt)}
    r = requests.get(cui_uri, params=query)
    r.encoding = 'utf-8'
    items = json.loads(r.text)
    jsonData = items["result"]
    # print(jsonData)
    name = jsonData["name"]
    semanticTypes = jsonData["semanticTypes"]
    semantic_type = ''
    for semanticType in semanticTypes:
        semantic_type += semanticType['name'] + ';'
    return name, semantic_type
