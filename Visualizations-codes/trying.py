import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

plt.rcParams['figure.max_open_warning'] = 50

# Load the data into a Pandas DataFrame
df = pd.read_csv('cleaned_sumo_data.csv')

# Define a dictionary that maps kimarite codes to their corresponding name.
kimarite_dict = {}

# Loop over each row in the DataFrame
for index, row in df.iterrows():

    # Get the kimarite for this row
    kimarite = row["kimarite"]

    # If this kimarite hasn't been seen before, add it to the dictionary
    if kimarite not in kimarite_dict:
        kimarite_dict[kimarite] = len(kimarite_dict) + 1

# Print the resulting dictionary
#print(kimarite_dict)

with open('kimarite_dict.json', 'w') as fp:
    json.dump(kimarite_dict, fp)

# Create a pivot table with the total number of wins for each rikishi and technique
pt = pd.pivot_table(df, index='rikishi1_shikona', columns='kimarite', values='basho', aggfunc='count')

# Aggregate the wins for each rikishi
pt['total_wins'] = pt.sum(axis=1)

# Sort the data by the total number of wins for each rikishi
pt = pt.sort_values(by='total_wins', ascending=False)

# Get the top 10 rikishi by total number of wins
top_rikishi = pt.iloc[:10].index.tolist()

# Subset the data for the top rikishi
pt_top = pt.loc[top_rikishi]

# Create the seaborn plot for top rikishi
sns.set_style('darkgrid')
plt.figure(figsize=(12, 6))
plot = sns.barplot(x=pt_top.index, y=pt_top['total_wins'], data=pt_top, palette='muted')
plot.set(title='Top 10 Rikishi by Total Wins', xlabel='Rikishi Shikona', ylabel='Total Number of Wins')
plot.set_xticklabels(plot.get_xticklabels(), rotation=45, horizontalalignment='right')

# Add labels to the bars
for p in plot.patches:
    plot.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

# Save the seaborn plot as a PNG file
plot.figure.savefig('top_10_rikishi.png', dpi=300)

# Create a pivot table with the total number of wins for each year and technique
pt = pd.pivot_table(df, index='basho', columns='kimarite', values='rikishi1_shikona', aggfunc='count')

# Convert the 'basho' column to integers
pt.index = pt.index.astype(int)

# Create a line plot with seaborn for each year
for year in range(pt.index.min(), pt.index.max() + 1):
    # Subset the data for the current year
    pt_year = pt.loc[pt.index == year]

    # Sort the data by number of wins
    pt_year = pt_year.sum().sort_values(ascending=False)

    # Get the top 10 techniques by number of wins
    top_techniques = pt_year.iloc[:10].index.tolist()

    # Subset the data for the top techniques
    pt_year_top = pt_year.loc[top_techniques]

    # Create the seaborn plot
    # Create the seaborn plot
    sns.set_style('darkgrid')
    plt.figure(figsize=(12, 6))
    plot = sns.barplot(x=[kimarite_dict[code] for code in pt_year_top.index], y=pt_year_top.values, data=pt_year_top, palette='muted')
    plot.set(title=f'Sumō Techniques with Most Wins in {year}', xlabel='Technique', ylabel='Number of Wins')
    plot.set_xticklabels(plot.get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.tight_layout()
    plt.legend(['Wins'], loc='upper right')

    # Add labels to the bars
    for p in plot.patches:
        plot.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), 
                      ha='center', va='center', xytext=(0, 10), textcoords='offset points')
        plot.annotate(p.get_x(), (p.get_x() + p.get_width() / 2., 0), 
                      ha='center', va='center', xytext=(0, 10), textcoords='offset points', rotation=45)
