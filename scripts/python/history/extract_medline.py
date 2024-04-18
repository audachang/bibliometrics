import pandas as pd
import re

def parse_medline(text):
    # Dictionary to hold the data
    data_dict = {}
    
    # Split the text into lines
    lines = text.strip().split('\n')
    
    # Variables to keep track of multiline values
    current_key = None
    current_value = []

    for line in lines:
        # Check if the line starts with a tag
        match = re.match(r'^([A-Z]+)\s?-\s(.*)', line)
        if match:
            # Save the previous key-value pair if there is one
            if current_key:
                data_dict[current_key] = ' '.join(current_value).strip()
            
            # Start a new key-value pair
            current_key = match.group(1)
            current_value = [match.group(2)]
        else:
            # This is a continuation of the previous tag's value
            current_value.append(line.strip())

    # Save the last key-value pair
    if current_key:
        data_dict[current_key] = ' '.join(current_value).strip()

    return data_dict

def load_medline_file(file_path):
    # Read the whole file into a single string
    with open(file_path, 'r') as file:
        file_contents = file.read()
    
    # Split the file contents into records, assuming records are separated by double newlines
    records = file_contents.strip().split('\n\n')
    
    # Parse each record into a dictionary
    parsed_records = [parse_medline(record) for record in records]
    
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(parsed_records)
    return df

# Usage
df = load_medline_file('../../data/pubmed-digitallea-set-2016-2019.txt')
print(df.head())
