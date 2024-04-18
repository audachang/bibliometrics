import pandas as pd

# Reading the top 5 keywords from a CSV file
keywords_csv_file_path = '../../data/extracted_keywords.csv'
keywords_df = pd.read_csv(keywords_csv_file_path, index_col=0)
top_5_keywords = keywords_df.iloc[:5].squeeze().tolist()

# Counting the frequency of the top 5 keywords in the records
records_df = pd.read_csv('../../data/records.csv')
keyword_frequencies = {keyword: records_df['TI'].str.contains(keyword, case=False, na=False).sum() for keyword in top_5_keywords}
