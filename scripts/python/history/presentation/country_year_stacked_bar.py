import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
df = pd.read_excel("country_by_year.xlsx")

# Pivot the data for 'Categories' for the bar plot
pivot_categories = df.pivot(index='Year', columns='Country', values='Journals').fillna(0)

# Pivot the data for 'NumPapers' for the line plot
pivot_numpapers = df.pivot_table(index='Year', values='NumPapers', aggfunc='sum')

# Initialize the matplotlib subplot object
fig, ax1 = plt.subplots(figsize=(12, 8))

# Colors for the stacked bar plot
colors = plt.cm.viridis(np.linspace(0, 1, len(pivot_categories.columns)))

# Plotting the stacked bar chart manually
bottom = np.zeros(len(pivot_categories))
for (i, column) in enumerate(pivot_categories.columns):
    ax1.bar(pivot_categories.index, pivot_categories[column], 
        bottom=bottom, label=column, color=colors[i])
    bottom += pivot_categories[column].values

# Labeling axes
ax1.set_xlabel('Year', fontsize=14)
ax1.set_ylabel('Journals', fontsize=14)
ax1.set_title('Publication Data by Year', fontsize=16)
ax1.tick_params(axis='both', which='major', labelsize=12)

# Create a secondary y-axis to plot the line plot
ax2 = ax1.twinx()
ax2.plot(pivot_numpapers.index, 
    pivot_numpapers['NumPapers'], color='k', 
    marker='o', linewidth=2, label='Total NumPapers')

# Secondary y-axis label
ax2.set_ylabel('Number of Papers', fontsize=14)
ax2.tick_params(axis='y', labelcolor='k')

# Collect all the handles and labels for the legend
handles, labels = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

# Combine handles and labels
handles.extend(handles2)
labels.extend(labels2)

# Create one legend with all handles and labels
ax1.legend(handles, labels, loc='upper left', title='Keywords and Total Papers')

plt.show()



## Group by Country and Year, and sum up the NumPapers for the defined year groups
grouped = df.groupby(
    ['Country', 
        pd.cut(df['Year'], 
            bins=[2015, 2019, 2024], 
            labels=['2016-2019', '2020-2024'])
        ]
    )['NumPapers'].sum().unstack(fill_value=0)


# Set up the bar locations and widths
bar_width = 0.35  # width of bars
index = np.arange(len(grouped))  # index for countries
fig, ax3 = plt.subplots()

# Plot each year group side by side
bars1 = ax3.bar(index - bar_width/2, grouped['2016-2019'], bar_width, label='2016-2019')
bars2 = ax3.bar(index + bar_width/2, grouped['2020-2024'], bar_width, label='2020-2024')

# Add some text for labels, title and axes ticks
ax3.set_xlabel('Country')
ax3.set_ylabel('NumPapers')
ax3.set_title('Number of Papers by Country and Year Group')
ax3.set_xticks(index)
ax3.set_xticklabels(grouped.index)
ax3.legend()
