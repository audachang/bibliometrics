import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = 'temp.xlsx'
data = pd.read_excel(file_path)

# Rename columns for clarity
data.columns = ['Keyword_2016_2019', 'Count_2016_2019', 'Keyword_2020_2023', 'Count_2020_2023']

# Prepare separate dataframes for each period with 'Period' marking
data_2016_2019 = data[['Keyword_2016_2019', 'Count_2016_2019']].rename(columns={'Keyword_2016_2019': 'Keyword', 'Count_2016_2019': 'Count'})
data_2020_2023 = data[['Keyword_2020_2023', 'Count_2020_2023']].rename(columns={'Keyword_2020_2023': 'Keyword', 'Count_2020_2023': 'Count'})
data_2016_2019['Period'] = '2016-2019'
data_2020_2023['Period'] = '2020-2023'

# Combine the two periods into a single DataFrame
combined_data = pd.concat([data_2016_2019, data_2020_2023])

# Create a pivot table
pivot_table = combined_data.pivot_table(values='Count', index='Period', columns='Keyword', aggfunc='sum', fill_value=0)
pivot_table = pivot_table.reindex(index=['2016-2019', '2020-2023'])

# Plotting the stacked bar chart with annotations
fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.get_cmap('tab10', len(pivot_table.columns))
bottoms = [0] * len(pivot_table.index)

for (i, (keyword, col)) in enumerate(zip(pivot_table.columns, colors(range(len(pivot_table.columns))))):
    values = pivot_table[keyword]
    ax.bar(pivot_table.index, values, bottom=bottoms, color=col, label=keyword)
    for j in range(len(values)):
        if values[j] != 0:
            ax.text(j, bottoms[j] + values[j]/2, \
                str(values[j]), ha='center', \
                va='center', color='white', fontsize = 18)

    bottoms = [sum(x) for x in zip(bottoms, values)]

ax.set_title('Counts of Keywords Across Periods with Labels', fontsize=16)
ax.set_xlabel('Period', fontsize=14)
ax.set_ylabel('Counts', fontsize=14)
ax.set_xticklabels(pivot_table.index, rotation=0)
ax.legend(title='Keywords', 
    bbox_to_anchor=(1.05, 1), 
    loc='upper left', fontsize=12)

plt.tight_layout()
plt.show()
