import pandas as pd

def main():
    # Load the keyword frequency data
    keyword_freq = pd.read_csv('../../data/keywords_frequencies.csv')
    
    # Sort the keywords by frequency and select the top 5
    top_keywords = keyword_freq.sort_values(by='Frequency', ascending=False).head(5)
    top_keywords_dict = dict(zip(top_keywords['Keyword'], top_keywords['Frequency']))
    print("Top 5 Keywords and Frequencies:", top_keywords_dict)

    # Load the original PubMed data
    pubmed_data = pd.read_csv('../../data/pubmed_2019-2024.csv')
    
    # Function to identify keywords in the title and match them with their global frequencies
    def keywords_in_title(title):
        title_lower = title.lower()
        return {keyword: top_keywords_dict[keyword] for keyword in top_keywords_dict if keyword in title_lower}

    # Apply the function to create a new column for the matched keywords and their frequencies
    pubmed_data['Keyword_Match_Details'] = pubmed_data['Title'].apply(keywords_in_title)
    
    # Filter to only include records where the 'Keyword_Match_Details' dictionary is not empty
    filtered_data = pubmed_data[pubmed_data['Keyword_Match_Details'].map(bool)]
    
    # Save the filtered data to a new CSV file
    filtered_data.to_csv('../../data/filtered_pubmed_records.csv', index=False)
    print(f"Filtered data saved: {filtered_data.shape[0]} records match the top 5 keywords.")
    
    return filtered_data

if __name__ == "__main__":
    filtered_results = main()
    print(filtered_results.head())  # Optionally print the first few results
