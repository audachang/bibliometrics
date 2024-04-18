import pandas as pd
import numpy as np
import random

# Set initial parameters
keywords = ['mobile', 'assessment', 'game', 'VR', 'collaborative learning']
years = range(2016, 2025)
base_number_of_papers = 5
min_growth, max_growth = -2, 6  # Minimum and maximum yearly growth

# Create the data structure with randomness and a new 'Categories' column
data = []
for year in years:
    for keyword in keywords:
        # If it's the first year, set the base number of papers
        if year == 2016:
            number_papers = base_number_of_papers
        else:
            # Get the number of papers for the same keyword in the previous year
            prev_year_papers = next(item['NumPapers'] for item in data if item['Year'] == year-1 and item['Keyword'] == keyword)
            # Randomly choose a growth number between min_growth and max_growth
            growth = np.random.randint(min_growth, max_growth)
            # Make sure the general trend is increasing
            number_papers = prev_year_papers + growth
        
        # The number of categories within each keyword is set to the number of papers
        # This can be changed to a random value not exceeding 'number_of_papers' if required
        categories = random.randint(0, number_papers)
        
        data.append({
            'Year': year, 
            'Keyword': keyword, 
            'NumPapers': number_papers, 
            'Categories': categories})


# The DataFrame 'df' now includes the 'Categories' column alongside the 'Year', 'Keyword', and 'Number of Papers' columns

# Create a DataFrame from the data
df = pd.DataFrame(data)
df.to_excel("keywords_by_year.xlsx")

