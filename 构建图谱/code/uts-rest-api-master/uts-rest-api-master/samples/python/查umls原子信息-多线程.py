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



apikey = "bb6e7f92-bf27-48df-99a1-369cbac50f7f"
version = "2020AB"
source = None
AuthClient = Authentication(apikey)

tgt = AuthClient.gettgt()
uri = "https://uts-ws.nlm.nih.gov"
ticket = AuthClient.getst(tgt)

def get_atom_code_2_cui(atom_code):
    # print(atom_code)
    query = {'ticket':AuthClient.getst(tgt), 'pageNumber':1}
    if 'AUI' in atom_code:
        r = requests.get(atom_code, params=query)
        r.encoding = 'utf-8'
        items = json.loads(r.text)
        cui_uri = items['result']['concept']
    else:
        r = requests.get(atom_code + "/atoms",params=query)
        r.encoding = 'utf-8'
        items  = json.loads(r.text)
        cui_uri = items['result'][0]['concept']
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
        pageCount = atom_items['pageCount']
        if pageCount == 0:
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






def get_atom_relation_from_cuis(cui_list, umls_name_list, csv_writer):
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
umls_name_list = ['abciximab', 'Acid Citrate Dextrose (ACD) Solutions', 'acetaminophen', 'acyclovir', 'adenosine', 'Albumins', 'alteplase', 'AmBisome', 'amikacin', 'Amino Acids', 'amiodarone', 'ampicillin', 'Ampicillin / Sulbactam', 'argatroban', 'atovaquone', 'atropine', 'autologous blood donor, whole blood', 'azithromycin', 'aztreonam', 'Bactrim', 'bivalirudin', 'Boost Glucose Control, chocolate', 'calcium gluconate', 'Carafate', 'caspofungin', 'cefazolin', 'cefepime', 'ceftazidime', 'ceftriaxone', 'Cell saver', 'ciprofloxacin', 'cisatracurium', 'clindamycin', 'colistin', 'Colloids', 'Coumadin', 'Cryoprecipitate', 'cyclosporine', 'daptomycin', 'dexmedetomidine', 'diazepam', 'phenytoin', 'diltiazem', 'dobutamine', 'dopamine', 'doxycycline', 'drotrecogin alfa', 'enoxaparin', 'Ensure (product)', 'Ensure Plus', 'epinephrine', 'eptifibatide', 'erythromycin', 'esmolol', 'factor VIIa', 'factor VIII', 'famotidine', 'fentanyl', 'Fresh frozen plasma', 'Fibersource HN', 'fluconazole', 'folic acid', 'fondaparinux', 'foscarnet', 'fosphenytoin', 'furosemide', 'ganciclovir', 'Genticin', 'Glucerna', 'haloperidol', 'heparin sodium', 'hetastarch', 'hydralazine', 'hydrochloric acid', 'hydromorphone', 'cilastatin / imipenem', 'Impact food supplement', 'Impact with Fiber', 'Insulin', 'ISOSOURCE', 'immunoglobulins, intravenous', 'K-Phos', 'potassium chloride', 'Keflex', 'levetiracetam', 'ketamine', 'labetalol', 'lansoprazole', 'levofloxacin', 'lidocaine', 'linezolid', 'Lipids', 'lorazepam', 'magnesium sulfate', 'mannitol', 'meperidine', 'meropenem', 'methadone hydrochloride', 'metoprolol', 'metronidazole', 'micafungin', 'midazolam', 'milrinone', 'morphine sulfate', 'Multivitamin preparation', 'Betamethasone Acet-Betamethasone Na Phos', 'nafcillin', 'naloxone', 'NEPRO', 'nesiritide', 'nicardipine', 'nitroglycerin', 'nitroprusside', 'norepinephrine', 'Novasource Renal', 'Nutren 2.0 Vanilla', 'NUTREN PULMONARY', 'NUTREN RENAL', 'octreotide', 'omeprazole', 'Resource Optisource', 'Transfusion of packed red blood cells', 'Packed red blood cells', 'pantoprazole', 'Penicillin G potassium:Mass:Pt:Dose:Qn', 'pentobarbital', 'Peptamen', 'Peptamen Bariatric', 'Peripheral parenteral nutrition', 'phenylephrine', 'piperacillin', 'piperacillin-tazobactam combination', 'Therapeutic apheresis; for plasma pheresis', 'Blood Platelets', 'PROBALANCE', 'procainamide', 'propofol', 'PULMOCARE', 'ranitidine', 'REPLETE', 'Replete with Fiber', 'rifampin', 'potassium bicarbonate / sodium bicarbonate', 'oseltamivir', 'thiamine', 'tirofiban', 'tobramycin', 'Parenteral Nutrition, Total', 'Two Cal HN', 'valganciclovir', 'vancomycin', 'Vasopressins', 'vecuronium', 'verapamil', 'vitamin K', 'Vivonex', 'voriconazole']
cui_list = ['C0288672', 'C4730099', 'C0000970', 'C0001367', 'C0001443', 'C0001924', 'C0032143', 'C0591076', 'C0002499', 'C0002520', 'C0002598', 'C0002680', 'C2930041', 'C0048470', 'C0165603', 'C0004259', 'C3650128', 'C0052796', 'C0004521', 'C0591139', 'C0168273', 'C4224267', 'C0006699', 'C0740157', 'C0537894', 'C0007546', 'C0055003', 'C0007559', 'C0007561', 'C1441512', 'C0008809', 'C1096766', 'C0008947', 'C0009316', 'C0009361', 'C0699129', 'C0443121', 'C0010592', 'C0057144', 'C0113293', 'C0012010', 'C0031507', 'C0012373', 'C0012963', 'C0013030', 'C0013090', 'C1170000', 'C0206460', 'C0218063', 'C0059375', 'C0014563', 'C0253563', 'C0014806', 'C0116569', 'C0015505', 'C0015506', 'C0015620', 'C0015846', 'C0016709', 'C2369942', 'C0016277', 'C0016410', 'C1098510', 'C0070895', 'C0244656', 'C0016860', 'C0017066', 'C0016898', 'C0726369', 'C0018546', 'C0037513', 'C0020352', 'C0020223', 'C0020259', 'C0012306', 'C0071972', 'C0726639', 'C0726641', 'C0021641', 'C0726747', 'C0085297', 'C1587981', 'C0032825', 'C0700517', 'C0377265', 'C0022614', 'C0022860', 'C0050940', 'C0282386', 'C0023660', 'C0663241', 'C0023779', 'C0024002', 'C0024480', 'C0024730', 'C0025376', 'C0066005', 'C0721688', 'C0025859', 'C0025872', 'C1120386', 'C0026056', 'C0128513', 'C0066814', 'C0301532', 'C4530929', 'C0027324', 'C0027358', 'C0727157', 'C0054015', 'C0028005', 'C0017887', 'C0028193', 'C0028351', 'C1170834', 'C0727244', 'C1996043', 'C1952578', 'C0028833', 'C0028978', 'C1653525', 'C0199962', 'C2316467', 'C0081876', 'C0366606', 'C0030883', 'C0359587', 'C3152426', 'C1527386', 'C0031469', 'C0031955', 'C0250480', 'C1144784', 'C0005821', 'C1875697', 'C0033216', 'C0033487', 'C0727620', 'C0034665', 'C4084254', 'C0727685', 'C0035608', 'C0718013', 'C0874161', 'C0039840', 'C0247025', 'C0040341', 'C0030548', 'C0728472', 'C0909381', 'C0042313', 'C0042413', 'C0242531', 'C0042523', 'C0042878', 'C0078391', 'C0393080']

from multiprocessing import Process

def foo(i):
    print ('say hi', i)

if __name__ == '__main__':
    for i in range(1,8):
        csv_writer = csv.writer(open(all_path.kg_file9+str(i) +'.csv', "a+", encoding="utf-8", newline=''))
        csv_writer.writerow(title)
        p = Process(target=get_atom_relation_from_cuis(cui_list[(i-1)*20:i*20], umls_name_list[(i-1)*20:i*20], csv_writer), args=(i,))
        p.start()
    p = Process(target=get_atom_relation_from_cuis(cui_list[(i - 1) * 20:i * 20], umls_name_list[(i - 1) * 20:i * 20],
                                                   csv.writer(open(all_path.kg_file9 + '8.csv', "a+", encoding="utf-8",
                                                                   newline=''))), args=(i,))
    p.start()
