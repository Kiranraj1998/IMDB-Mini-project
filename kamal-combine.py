
import pandas as pd
import glob

# Get a list of all csv files in the directory
csv_files = glob.glob('C:/Guvi/IMDB-Mini-project/csv_files/*.csv')
#C:\Guvi\IMDB-Mini-project\csv_files
# Create an empty list to store DataFrames
dfs = []

# Loop through the files and append them to the list
for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined DataFrame to a new CSV file
#combined_df.to_csv('combined_file.csv', index=False)

# Function to clean votes (convert 'K' to thousands)
def clean_votes(vote_str):
    if pd.isna(vote_str):
        return None
    vote_str = str(vote_str).strip()
    if 'K' in vote_str:
        num = float(vote_str.replace('K', '')) * 1000
    else:
        num = float(vote_str)
    # Return as int if whole number, float otherwise
    return int(num) if num.is_integer() else num
    

# Function to convert duration to minutes
def convert_duration(duration_str):
    if pd.isna(duration_str):
        return None
    
    hours = 0
    minutes = 0
    
    if 'h' in duration_str:
        parts = duration_str.split()
        for part in parts:
            if 'h' in part:
                hours = int(part.replace('h', ''))
            elif 'm' in part:
                minutes = int(part.replace('m', ''))
    elif 'm' in duration_str:
        minutes = int(duration_str.replace('m', ''))
    
    return hours * 60 + minutes

# Apply cleaning functions to the DataFrame
combined_df['Votes'] = combined_df['Votes'].apply(clean_votes)
combined_df['Duration_Minutes'] = combined_df['Duration'].apply(convert_duration)

# Save the combined and cleaned DataFrame to a new CSV file
combined_df.to_csv('combined_cleaned_file.csv', index=False)

print("Successfully combined and cleaned the files. Saved as 'combined_cleaned_file.csv'")
print(f"Total movies: {len(combined_df)}")