#################################################################################
# usage of the script
# usage: python search-terms.py -k APIKEY -v VERSION -s STRING
# see https://documentation.uts.nlm.nih.gov/rest/search/index.html for full docs
# on the /search endpoint
#################################################################################

from __future__ import print_function
from Authentication import *
import requests
import json

# parser = argparse.ArgumentParser(description='process user given parameters')
# #parser.add_argument("-u", "--username", required =  True, dest="username", help = "enter username")
# #parser.add_argument("-p", "--password", required =  True, dest="password", help = "enter passowrd")
# parser.add_argument("-k", "--apikey", required = True, dest = "apikey", help = "enter api key from your UTS Profile")
# parser.add_argument("-v", "--version", required =  False, dest="version", default = "current", help = "enter version example-2015AA")
# parser.add_argument("-s", "--string", required =  True, dest="string", help = "enter a search term, like 'diabetic foot'")
# args = parser.parse_args()
#username = args.username
#password = args.password

# apikey = args.apikey
# version = args.version
# string = args.string

import all_path
import csv
apikey = "bb6e7f92-bf27-48df-99a1-369cbac50f7f"
version = "2020AB"
csv_reader1 = csv.reader(open(all_path.drug_frecuency_category_file, 'r', encoding='gbk'))
csv_reader2 = csv.reader(open(all_path.drug_regular_file, 'r', encoding='gbk'))
csv_writer = csv.writer(open(all_path.drug_with_cui_link_file, "w", encoding="gbk", newline=''))
csv_writer.writerow(["drug_item_label", "drug_regular_label", "umls_name", "drug_item_category", "drug_category_lx",
                     "count", "cui", "Source Vocabulary"])


drug_item_list_to_others = {}
search_result = {}

line = 0
for line in csv_reader2:
    if line==0:
        line += 1
        continue
    drug_item_label = line[0]
    drug_regular_label = line[1]
    drug_item_list_to_others[drug_item_label]={"drug_regular_label":drug_regular_label}

line = 0
for line in csv_reader1:
    if line==0:
        line += 1
        continue
    drug_item_label = line[0]
    drug_item_category = line[1]
    count = line[2]
    drug_category_lx = line[3]
    try:
        drug_item_list_to_others[drug_item_label]["drug_item_category"] = drug_item_category
        drug_item_list_to_others[drug_item_label]["count"] = count
        drug_item_list_to_others[drug_item_label]["drug_category_lx"] = drug_category_lx
    except:
        continue


for drug_item_label in drug_item_list_to_others.keys():
    string = drug_item_list_to_others[drug_item_label]["drug_regular_label"]
    print(string)
    if string in search_result.keys():
        result = search_result[string]
        csv_writer.writerow([drug_item_label, string, result["name"],
         drug_item_list_to_others[drug_item_label]["drug_item_category"],
         drug_item_list_to_others[drug_item_label]["drug_category_lx"],
         drug_item_list_to_others[drug_item_label]["count"], result["ui"], result["rootSource"]])
        continue

    uri = "https://uts-ws.nlm.nih.gov"
    content_endpoint = "/rest/search/"+version
    ##get at ticket granting ticket for the session
    AuthClient = Authentication(apikey)
    tgt = AuthClient.gettgt()
    pageNumber=0

    while True:
    ##generate a new service ticket for each page if needed
        ticket = AuthClient.getst(tgt)
        pageNumber += 1
        query = {'string':string,'ticket':ticket, 'pageNumber':pageNumber}
        #query['includeObsolete'] = 'true'
        #query['includeSuppressible'] = 'true'
        #query['returnIdType'] = "sourceConcept"
        #query['sabs'] = "SNOMEDCT_US"
        r = requests.get(uri+content_endpoint,params=query)
        r.encoding = 'utf-8'
        items  = json.loads(r.text)
        print(items)

        jsonData = items["result"]
        #print (json.dumps(items, indent = 4))

        print("Results for page " + str(pageNumber)+"\n")
        if jsonData["results"][0]["ui"] == "NONE":
            csv_writer.writerow([drug_item_label, string,"",
                                 drug_item_list_to_others[drug_item_label]["drug_item_category"],
                                 drug_item_list_to_others[drug_item_label]["drug_category_lx"],
                                 drug_item_list_to_others[drug_item_label]["count"], "", ""])
            break
        result = jsonData["results"][0]
        search_result[string] = {"name":result["name"], "ui":result["ui"], "rootSource":result["rootSource"]}
        csv_writer.writerow([drug_item_label, string,result["name"],
                                 drug_item_list_to_others[drug_item_label]["drug_item_category"],
                                 drug_item_list_to_others[drug_item_label]["drug_category_lx"],
                                 drug_item_list_to_others[drug_item_label]["count"], result["ui"], result["rootSource"]])

        break
        # for result in jsonData["results"]:
        #   try:
        #     print("ui: " + result["ui"])
        #   except:
        #     NameError
        #   try:
        #     print("uri: " + result["uri"])
        #   except:
        #     NameError
        #   try:
        #     print("name: " + result["name"])
        #   except:
        #     NameError
        #   try:
        #     print("Source Vocabulary: " + result["rootSource"])
        #   except:
        #     NameError
        #
        #   print("\n")
        #
        #
        # ##Either our search returned nothing, or we're at the end
        # if jsonData["results"][0]["ui"] == "NONE":
        #     break
        # print("*********")

    
    
    
    
    

