import pandas as pd
import numpy as np
import random

# Define the range of years and countries
years = range(2016, 2025)
countries = [
    'USA', 'Taiwan', 'China', 'Japan', 'Korea', 'UK', 'Nederland',
    'Germany', 'France', 'Italy', 'Canada', 'Australia', 'India',
    'Brazil', 'Russia', 'Mexico', 'Spain', 'South Africa', 'Sweden', 'Norway'
]

# Initialize the list for storing data
data = []

# Generate random data for number of papers for each country and each year
for country in countries:
    for year in years:
        num_papers = random.randint(50, 500)  # Randomly generate the number of papers (example range)
        data.append({
            'Country': country,
            'Year': year,
            'NumPapers': num_papers
        })

# Convert the list to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel('20countryXyear.xlsx', index=False)

# Print out the first few rows of the dataframe to check
print(df.head())

