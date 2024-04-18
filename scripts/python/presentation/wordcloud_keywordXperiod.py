import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the data
data = pd.read_excel('temp.xlsx')  # Update the path to your Excel file
data.columns = ['Keyword_2016_2019', 'Count_2016_2019', 'Keyword_2020_2023', 'Count_2020_2023']

# Prepare the data for each period
data_2016_2019 = data[['Keyword_2016_2019', 'Count_2016_2019']].rename(columns={'Keyword_2016_2019': 'Keyword', 'Count_2016_2019': 'Count'})
data_2020_2023 = data[['Keyword_2020_2023', 'Count_2020_2023']].rename(columns={'Keyword_2020_2023': 'Keyword', 'Count_2020_2023': 'Count'})
data_2016_2019['Period'] = '2016-2019'
data_2020_2023['Period'] = '2020-2023'

# Function to apply frame settings to an axis
def set_frame_style(ax, color='black', linewidth=2):
    for spine in ax.spines.values():
        spine.set_color(color)
        spine.set_linewidth(linewidth)
    return ax



# Function to generate and plot word clouds with black frames
def plot_word_clouds(data1, data2, title1, title2):
    # Setting up the figure and subplots
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    # Generate and display the word cloud for 2016-2019
    word_frequencies1 = {row['Keyword']: int(row['Count']) for index, row in data1.iterrows()}
    wordcloud1 = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_frequencies1)
    axes[0].imshow(wordcloud1, interpolation='bilinear')
    axes[0].set_title(title1, fontsize=18)
    axes[0].axis("off")
    axes[0] = set_frame_style(axes[0])  # Apply frame style

    # Generate and display the word cloud for 2020-2023
    word_frequencies2 = {row['Keyword']: int(row['Count']) for index, row in data2.iterrows()}
    wordcloud2 = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_frequencies2)
    axes[1].imshow(wordcloud2, interpolation='bilinear')
    axes[1].set_title(title2, fontsize=18)
    axes[1].axis("off")
    axes[1] = set_frame_style(axes[1])  # Apply frame style

    plt.tight_layout()
    return axes


# Call the function with both periods
axes = plot_word_clouds(
    data_2016_2019, data_2020_2023, 
    '2016-2019', '2020-2023')