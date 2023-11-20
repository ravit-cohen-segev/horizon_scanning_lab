import pandas as pd
import requests
import xml.etree.ElementTree as ET

df = pd.read_parquet(r'C:\Users\Ravit\Downloads\000_00.gz.parquet') 

# In[]
def get_doi_from_oai(oai, base_url):
 
    params = {
        'verb': 'GetRecord',
        'metadataPrefix': 'arXiv',
        'identifier': oai
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        print("Error:", response.status_code)
        return None

    # Parse the XML response
    root = ET.fromstring(response.content)

    # Namespace for OAI
    namespaces = {
        'oai': 'http://www.openarchives.org/OAI/2.0/',
        'arxiv': 'http://arxiv.org/OAI/arXiv/'
    }

    # Search for the DOI in the XML structure
    doi_element = root.find(".//arxiv:doi", namespaces=namespaces)
    
    if doi_element is not None:
        return doi_element.text
    else:
        print("DOI not found for the given OAI.")
        return None

# In[]
base_urls = ["https://arxiv.org/oai2"]

# Test
doi = get_doi_from_oai('oai:dspace.univer.kharkov.ua:123456789/6879', base_urls[0])
if doi:
    print("DOI:", doi)
    
# In[]
import re

oai_list = df['oai'].to_list()

pattern = r'oai:(.*?):'
base_urls = set()  # using a set to ensure uniqueness

for oai in oai_list:
    match = re.search(pattern, oai)
    if match:
        base_urls.add(match.group(1))

print(base_urls)

# In[]

#Extract base URL from an OAI identifier.

def extract_base_url(oai_identifier):
    """
    Extract base URL from an OAI identifier.
    """
    parts = oai_identifier.split(':')
    if len(parts) > 2:
        return parts[1]
    else:
        return None

# Sample list of OAI identifiers
oai_identifiers = [
    "oai:iris.unimore.it:11380/21757",
    "oai:arXiv.org:cs/0502064",
    "oai:waseda.repo.nii.ac.jp:00022245",
    "oai:repository.ubn.ru.nl:2066/159561",
    "oai:aisel.aisnet.org:pacis1997-1097",
    "oai:digitalcommons.mtu.edu:bryo-ecol-subchapter-1008",
    "oai:elib.dlr.de:122756",
    "oai:digitalcommons.library.umaine.edu:findingaid-1001",
    "oai:mu.repo.nii.ac.jp:00001294",
    "oai:diposit.ub.edu:2445/99593",
    "oai:digitalcommons.wpi.edu:etd-theses-1763",
    "oai:repository.usmf.md:20.500.12710/10896",
    "oai:dspace.univer.kharkov.ua:123456789/6879"
]

base_urls = set()  # Use a set to store unique base URLs

for oai_id in oai_identifiers:
    base_url = extract_base_url(oai_id)
    if base_url:
        base_urls.add(base_url)

print(base_urls)
