from Bio import Entrez
from Bio import Medline
import pandas as pd
import numpy as np
import csv
import os
import re

def scraping_pubmed(term, email):
    search_term = term
    Entrez.email = email
    
    handle = Entrez.egquery(term=search_term)
    record = Entrez.read(handle)
    for row in record["eGQueryResult"]:
        if row['DbName']=="pubmed":
            paper_numbers=row["Count"]
                       
    handle = Entrez.esearch(db="pubmed",
                            term=search_term,
                            retmax=paper_numbers,
                            #mindate = '2000/01/01',
                            #maxdate = '2015/12/31'
                            )
    record = Entrez.read(handle)
    handle.close()
    idlist=record["IdList"]
    
    
    records = []
    for i in range(0, len(idlist), 10000):
        j = i + 10000
        if j >= len(idlist):
            j = len(idlist)
            
        handle=Entrez.efetch(db="pubmed", id=idlist[i:j],
                             rettype='medline', retmode='text')
        record=Medline.parse(handle)
 
        
        for r in record:
            records.append(r)
            
    header = ['PMID', 'Title', 'Abstract', 'Key_words', 'Authors', 'Journal', 'Year', 'Month', 'Source','Country']
    
    with open('Processing.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        
        # write the header
        writer.writerow(header)
        
        # write the data
        for paper in records:
            try:
                PMID = paper['PMID']
            except:
                PMID = None
                
            try:
                Title = paper['TI']
            except:
                try:
                    Title = paper['TT'] 
                except:
                    try:
                        Title = paper['BTI']
                    except:
                        Title = None
            
            try:
                Abstract = paper['AB']
            except:
                Abstract = None
            
            try:
                Key_words = paper['MH']
            except:
                try:
                    Key_words = paper['OT']
                except:
                    Key_words = None
                    
            try:
                Authors = paper['FAU']
            except:
                try:
                    Authors = paper['FED']
                except:
                    Authors = None
                
            try:
                Journal = paper['TA']
            except:
                Journal = None
        
            try:
                Year = paper['EDAT'].split('/')[0]
            except:
                Year = None
            
            try:
                Month = paper['EDAT'].split('/')[1]
            except:
                Month = None
            
            try:
                Source = paper['SO']
            except:
                Source = None
            
            try:
                Country = paper['AD'][0].split(',')[-1][:-1].lstrip()
                regex = re.compile('[\w\.-]+@[\w\.-]+(\.[\w]+)+')
                if re.search(regex, Country):
                    Country = Country.split(".")[0]
                else:
                    Country = Country
                
                #Country = paper['AD'][0].split(',')[-1][:-1].split('.')[0].lstrip()
            except:
                Country = None
            
            data = [PMID, Title, Abstract, Key_words, Authors, Journal, Year, Month, Source, Country]
            writer.writerow(data)
            
    df = pd.read_csv('Processing.csv')
    print('A total of {} articles were retrieved from PubMed by searching the term "{}".'.format(df.shape[0], term))    
    filename =format('_'.join(search_term.split(' '))) + '.csv'
    if os.path.exists(filename):
        os.remove(filename)
        os.rename('Processing.csv',filename)
    else:
        os.rename('Processing.csv',filename)

if __name__ == "__main__":
    scraping_pubmed("digital learning",'audachang@gmail.com')