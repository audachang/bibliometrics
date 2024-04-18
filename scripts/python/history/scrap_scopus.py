import csv
import time
from pybliometrics.scopus import ScopusSearch, AbstractRetrieval
from tqdm import tqdm

query = 'TITLE-ABS-KEY("brain") AND TITLE-ABS-KEY("psychology") AND PUBYEAR AFT 2015 AND PUBYEAR BEF 2025'

print("querying Scopus...")
search_result = ScopusSearch(query)
eids = search_result.get_eids()


# Print the total number of matching articles
print(f"Total number of matching articles: {len(eids)}")

# Confirm to proceed with the download
proceed = input("Proceed with downloading details? (y/n): ")
if proceed.lower() != 'y':
    print("Download canceled.")
    exit()

with open('scopus_results.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['EID', 'Title', 'Authors', 'Year', 'DOI', 'Abstract'])
    
    # Define the size of each batch (25 is typical to stay within typical API limits)
    batch_size = 25  

    # Setup tqdm progress bar for the whole process
    pbar = tqdm(total=len(eids), desc="Processing articles", unit="article")

    for i in range(0, len(eids), batch_size):
        batch = eids[i:i+batch_size]
        for eid in batch:
            try:
                abstract = AbstractRetrieval(eid, view="FULL")
                # Concatenate author names
                authors = ', '.join([author.given_name + ' ' + author.surname for author in abstract.authors])
                # Write row with all data
                writer.writerow([eid, abstract.title, authors, abstract.coverDate[:4], abstract.doi, abstract.abstract])
            except Exception as e:
                print(f"Failed to process {eid}: {str(e)}")
            finally:
                pbar.update(1)  # Update progress bar after each article
        
        #time.sleep(1)  # Sleep to avoid hitting the rate limit
    
    pbar.close()  # Close the progress bar after all items are processed
