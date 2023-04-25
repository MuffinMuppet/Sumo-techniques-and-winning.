import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data into a Pandas DataFrame
df = pd.read_csv('cleaned_sumo_data.csv')

# Get the unique techniques
unique_techniques = df['kimarite'].unique()

# Create a pivot table with the total number of wins for each year and technique
pt = pd.pivot_table(df, index='basho', columns='kimarite', values='rikishi1_shikona', aggfunc='count')

# Plot the stacked bar chart using Seaborn
sns.set_style('whitegrid')
ax = pt.plot(kind='bar', stacked=True, figsize=(12, 8), color=sns.color_palette('Set3', len(unique_techniques)))

# Set the axis labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Number of Wins')
ax.set_title('Wins by Technique and Year')

# Save the plot to a file
plt.savefig('technique_wins_by_year.png')

# Show the plot
plt.show()
