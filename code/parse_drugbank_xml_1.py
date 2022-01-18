from lxml import etree
from io import StringIO
from collections import defaultdict
import csv
import gzip
import xml.etree.ElementTree as ET
# Parse XML
from pytz import unicode

# print len(root), 'drugs'


tree = ET.parse(open(r'C:\Users\pinkpigma\pinkpigma的同步盘\KDD研二上\可解释性框架-工作\数据\full database.xml', encoding='utf-8'))
root = tree.getroot()
#######################################################################
# Iterate over drugs
drug2attrib = defaultdict(dict)
# drugbank_id -> {'drugname', 'drug_type', 'groups', 'targets/enzymes/transporters': [_id, _actions]}

target2attrib = defaultdict(dict)
enzyme2attrib = defaultdict(dict)
transporter2attrib = defaultdict(dict)
# drugbank_target_id -> {'gene', 'name', 'organism', 'taxonomy_id', 'uniprot_id', 'genbank_gene_id', 'genbank_protein_id', 'hgnc_id'}

tag_prefix = '{http://www.drugbank.ca}'

for child in root:
    print(child)
    break

