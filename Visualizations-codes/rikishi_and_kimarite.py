import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data into a Pandas DataFrame
df = pd.read_csv('cleaned_sumo_data.csv')

# Create a pivot table with the total number of wins for each rikishi and technique
pt = pd.pivot_table(df, index='rikishi1_shikona', columns='kimarite', values = 'basho', aggfunc='count')

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
plt.tight_layout()

# Save the seaborn plot as a PNG file
plot.figure.savefig('top_10_rikishi.png', dpi=300)

# Create a pivot table with the total number of wins for each year and technique
pt = pd.pivot_table(df, index='basho', columns='kimarite', values = 'rikishi1_shikona', aggfunc='count')

# Convert the 'basho' column to integers
pt.index = pt.index.astype(int)

# Create a line plot with seaborn for each year
for year in range(pt.index.min(), pt.index.max()+1):
    # Subset the data for the current year
    pt_year = pt.loc[pt.index == year]
    
    # Sort the data by number of wins
    pt_year = pt_year.sum().sort_values(ascending=False)
    
    # Get the top 10 techniques by number of wins
    top_techniques = pt_year.iloc[:10].index.tolist()
    
    # Subset the data for the top techniques
    pt_year_top = pt_year.loc[top_techniques]
    
    # Create the seaborn plot
    sns.set_style('darkgrid')
    plt.figure(figsize=(12, 6))
    plot = sns.barplot(x=pt_year_top.index, y=pt_year_top.values, data=pt_year_top, palette='muted')
    plot.set(title=f'Sumō Techniques with Most Wins in {year}', xlabel='Technique', ylabel='Number of Wins')
    plot.set_xticklabels(plot.get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.tight_layout()
    plt.legend(['Wins'], loc='upper right')
    
    # Save the seaborn plot as a PNG file
    plot.figure.savefig(f'{year}_sumo_wins.png', dpi=300)
    
    # Close the current figure to avoid memory issues
    plt.show()
