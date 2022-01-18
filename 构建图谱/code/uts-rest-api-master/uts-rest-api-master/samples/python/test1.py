#coding=utf-8
from Authentication import *
import requests
import json
import all_path, csv
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf8")  ## encoding 的参数写成网站的编码格式即可





apikey = "bb6e7f92-bf27-48df-99a1-369cbac50f7f"
version = "2020AB"
source = None
AuthClient = Authentication(apikey)

tgt = AuthClient.gettgt()
uri = "https://uts-ws.nlm.nih.gov"
ticket = AuthClient.getst(tgt)




##generate a new service ticket for each page if needed


cui_uri = ''


query = {'ticket':AuthClient.getst(tgt), 'pageNumber':1}
# r = requests.get("https://uts-ws.nlm.nih.gov/rest/content/2021AA/source/RXNORM/152626",params=query)
# query = {'ticket':AuthClient.getst(tgt), 'pageNumber':1, 'string':'clindamycin 120 MG/ML'}
# r = requests.get("https://uts-ws.nlm.nih.gov/rest/search/2020AB/",params=query)

r = requests.get("https://uts-ws.nlm.nih.gov/rest/content/2020AB/CUI/C0002645/atoms", params=query)

r.encoding = 'utf-8'
items  = json.loads(r.text)
print(items)
for item in items['result']:
    print(item)
    print(item['code'].split('/')[-2])








