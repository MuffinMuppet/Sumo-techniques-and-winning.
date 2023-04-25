import pandas as pd
import glob

def clean_data(df):
    """
    Cleans the given DataFrame by removing duplicates and converting data types.
    """
    # Remove duplicate rows
    df.drop_duplicates(inplace=True)
    
    # Convert data types of columns
    df = df.astype({
        'index': 'int32',
        'basho': 'category',
        'day': 'int8',
        'rikishi1_id': 'int32',
        'rikishi1_rank': 'category',
        'rikishi1_shikona': 'object',
        'rikishi1_result': 'object',
        'rikishi1_win': 'bool',
        'kimarite': 'category',
        'rikishi2_id': 'int32',
        'rikishi2_rank': 'category',
        'rikishi2_shikona': 'object',
        'rikishi2_result': 'object',
        'rikishi2_win': 'bool'
    })
    
    
    # Suggestion: remove any rows where both Rikishi1_Win and Rikishi2_Win are False
    # This is because the dataset only contains records for matches where one wrestler wins and one loses
    df = df.loc[(df['rikishi1_win'] == True) | (df['rikishi2_win'] == True)]
    
    return df

# Load all CSV files in the specified directory
path = r'C:\Users\aoyedira\Downloads\archive'
all_files = glob.glob(path + "/*.csv")

# Concatenate all dataframes into one
dfs = [pd.read_csv(filename, usecols=['index', 'basho', 'day', 'rikishi1_id', 'rikishi1_rank', 'rikishi1_shikona', 'rikishi1_result', 'rikishi1_win', 'kimarite', 'rikishi2_id', 'rikishi2_rank', 'rikishi2_shikona', 'rikishi2_result', 'rikishi2_win']) for filename in all_files]
df = pd.concat(dfs, ignore_index=True)

# Clean the data
df = clean_data(df)

# Output the cleaned DataFrame
print(df.head())

df.to_csv('cleaned_sumo_data.csv', index=False)
