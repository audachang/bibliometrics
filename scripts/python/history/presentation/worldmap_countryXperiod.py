import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Assuming 'df' and 'world' are already loaded and merged as shown in previous steps

# Load the data
df = pd.read_excel('20countryXyear.xlsx')  # Adjust the path to your actual file

# Define the year groups by creating a new column 'Year Group'
df['Year Group'] = pd.cut(df['Year'], bins=[2015, 2019, 2024], labels=['2016-2019', '2020-2024'], right=True)

# Aggregate data
grouped = df.groupby(['Country', 'Year Group'])['NumPapers'].sum().reset_index()

# Pivot the table to have year groups as columns
pivot_df = grouped.pivot(index='Country', columns='Year Group', values='NumPapers').fillna(0)

# Load the world map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the world GeoDataFrame with the pivoted data
world = world.merge(pivot_df, how="left", left_on="name", right_on="Country")

# Determine consistent color scale across both maps
vmin, vmax = world[['2016-2019', '2020-2024']].min().min(), world[['2016-2019', '2020-2024']].max().max()

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Plot 2016-2019 data
world.plot(column='2016-2019', ax=ax1, legend=False,
           vmin=vmin, vmax=vmax, cmap='viridis')
ax1.set_title('Papers Published 2016-2019')
ax1.set_axis_off()

# Plot 2020-2024 data
world.plot(column='2020-2024', ax=ax2, legend=False,
           vmin=vmin, vmax=vmax, cmap='viridis')
ax2.set_title('Papers Published 2020-2024')
ax2.set_axis_off()

# Add a single colorbar
fig.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.87, 0.15, 0.03, 0.7])
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax))
fig.colorbar(sm, cax=cbar_ax)

plt.show()
