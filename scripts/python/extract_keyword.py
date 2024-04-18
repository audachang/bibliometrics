import pandas as pd
from collections import Counter
import re

def extract_keywords(title):
    # Filter out non-alphabetic characters and split the title into words
    words = re.sub("[^a-zA-Z]", " ", title).lower().split()
    return [word for word in words if len(word) > 3]  # Keep words longer than 3 characters

def main():
    data = pd.read_csv('../../data/pubmed_2019-2024.csv')
    
    # Apply keyword extraction to the 'Title' column
    data['Keywords'] = data['Title'].apply(extract_keywords)
    
    # Apply Counter to get frequencies of keywords in each title
    data['Keyword_Frequency'] = data['Keywords'].apply(lambda x: Counter(x))
    
    # Initialize list to collect rows for the new DataFrame
    rows = []
    
    # Create rows for each keyword and its frequency
    for index, row in data.iterrows():
        for keyword, frequency in row['Keyword_Frequency'].items():
            rows.append({'Keyword': keyword, 'Frequency': frequency})
    
    # Use pandas.concat to form the DataFrame from rows
    keyword_records = pd.concat([pd.DataFrame([row]) for row in rows], ignore_index=True)
    
    # Save the keywords and their frequencies to a new CSV file
    keyword_records.to_csv('../../data/keywords_frequencies.csv', index=False)
    print("Keywords and frequencies have been saved to keywords_frequencies.csv")

if __name__ == "__main__":
    main()
