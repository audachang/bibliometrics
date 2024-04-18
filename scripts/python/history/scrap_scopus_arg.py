import csv
import sys
import time
from pybliometrics.scopus import ScopusSearch, AbstractRetrieval
from pybliometrics.scopus.exception import Scopus429Error
from tqdm import tqdm

def robust_abstract_retrieval(eid, base_delay=60, max_retries=5):
    """Attempts to retrieve article details with retries and respects rate limits."""
    for attempt in range(max_retries):
        try:
            abstract = AbstractRetrieval(eid, view="FULL")
            return abstract
        except Scopus429Error:
            wait_time = base_delay * (2 ** attempt)  # Exponential back-off
            print(f"Rate limit exceeded, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(base_delay * (2 ** attempt))  # Exponential back-off
            else:
                print(f"Failed to retrieve data for EID {eid} after {max_retries} attempts due to {str(e)}")
                raise
    raise Exception(f"Failed to retrieve data for EID {eid} after maximum retries.")

if len(sys.argv) < 2:
    print("Usage: python scrap_scopus.py <TITLE-ABS-KEY>")
    sys.exit(1)

title_abs_key = sys.argv[1]
query = f'TITLE-ABS-KEY({title_abs_key}) AND PUBYEAR AFT 2015 AND PUBYEAR BEF 2025'

print("Querying Scopus...")
search_result = ScopusSearch(query)
eids = search_result.get_eids()

# Print the total number of matching articles
print(f"Total number of matching articles: {len(eids)}")

# Confirm to proceed with the download
proceed = input("Proceed with downloading details? (y/n): ")
if proceed.lower() != 'y':
    print("Download canceled.")
    sys.exit()

droot = '../../data/scopus'
filename = f'{droot}/scopus_results_{title_abs_key.replace(" ", "_")}.csv'
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['EID', 'Title', 'Authors', 'Affiliations', 'Year', 'DOI', 'Abstract'])
    
    # Define the size of each batch (25 is typical to stay within typical API limits)
    batch_size = 25  

    # Setup tqdm progress bar for the whole process
    pbar = tqdm(total=len(eids), desc="Processing articles", unit="article")

    for i in range(0, len(eids), batch_size):
        batch = eids[i:i+batch_size]
        for eid in batch:
            try:
                abstract = robust_abstract_retrieval(eid)
                authors = ', '.join([author.given_name + ' ' + author.surname for author in abstract.authors])
                affiliations = '; '.join([aff.name for aff in abstract.affiliation])
                writer.writerow([eid, abstract.title, authors, affiliations, abstract.coverDate[:4], abstract.doi, abstract.abstract])
            except Exception as e:
                print(f"Failed to process {eid}: {str(e)}")
            finally:
                pbar.update(1)  # Update progress bar after each article
    
    pbar.close()  # Close the progress bar after all items are processed
