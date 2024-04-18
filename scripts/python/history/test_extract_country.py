import bibtexparser
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from tqdm import tqdm
import pandas as pd
from itertools import combinations
from collections import Counter
import re
import usaddress


def massage_data(address):
    '''Pre process address string to remove new line characters, add comma punctuations etc.'''
    cleansed_address1 = re.sub(r'(,)(?!\s)', ', ', address)
    cleansed_address2 = re.sub(r'(\\n)', ', ', cleansed_address1)
    cleansed_address3 = re.sub(r'(?!\s)(-)(?!\s)', ' - ', cleansed_address2)
    cleansed_address = re.sub(r'\.', '', cleansed_address3)
    cleansed_address = cleansed_address.split('\n')
  
    return cleansed_address

def get_countries_from_address(address):
    '''Parse the preprocessed address string to extract country'''
    cleaned_address = massage_data(address)
    parsed_address = usaddress.tag(cleaned_address)
    country = None
    for component, label in parsed_address:
        if label == 'CountryName':
            country = component
            break
    return country

def massage_data(address):
    '''Pre process address string to remove new line characters, add comma punctuations etc.'''
    cleansed_address1 = re.sub(r'(,)(?!\s)', ', ', address)
    cleansed_address2 = re.sub(r'(\\n)', ', ', cleansed_address1)
    cleansed_address3 = re.sub(r'(?!\s)(-)(?!\s)', ' - ', cleansed_address2)
    cleansed_address = re.sub(r'\.', '', cleansed_address3)
    #cleansed_address = cleansed_address.split('\n')
    return cleansed_address

def get_countries_from_address(address):
    '''Parse the preprocessed address string to extract country'''
    cleaned_address = massage_data(address)
    parsed_address = usaddress.tag(cleaned_address)
    print(parsed_address)
    country = None
    for component, label in parsed_address:
        if label == 'CountryName':
            country = component
            break
    return country

def get_bib_entries(entry):
    """Process each entry in the .bib file to extract countries from affiliations."""
    affiliation_key = 'affiliation' if 'affiliation' in entry else 'affiliations' if 'affiliations' in entry else None
    records = []
    if affiliation_key:
        addresses = entry[affiliation_key].split('\n')
        #print(addresses)
        if isinstance(addresses, list):
            for address in addresses:
		print(address)
                country = get_countries_from_address(address)
                record = {'title': entry.get('title', 'No title provided'),
                          'journal': entry.get('journal', 'No journal provided'),
                          'country': country}
                records.append(record)
        else:
            country = get_countries_from_address(addresses)
            record = {'title': entry.get('title', 'No title provided'),
                      'journal': entry.get('journal', 'No journal provided'),
                      'country': country}
            records.append(record)
    else:
        record = {'title': entry.get('title', 'No title provided'),
                  'journal': entry.get('journal', 'No journal provided'),
                  'country': 'No affiliation info'}
        records.append(record)

    return records



# Example usage
droot = '../../data/wos'
filename = f'{droot}/wos_fMRI_2016-2024.bib'  # Update the path to your .bib file
with open(filename) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

address = bib_database.entries[0]['affiliation']
cleaned_address = massage_data(address)

get_countries_from_address(bib_database.entries[0]['affiliation'])
