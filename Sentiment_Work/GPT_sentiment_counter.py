import os
import pandas as pd

def process_headlines(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith(('CNN -', 'FOX -', 'NBC -')):
                outlet, content = line.split(' - ', 1)
                figure_info, headline = content.split(': ', 1)
                figure = figure_info.split(' ')[0]
            else:
                sentiments = line.split(') ')
                for sentiment_info in sentiments:
                    if ':' in sentiment_info:  # Check if sentiment_info contains a colon
                        try:
                            figure_sentiment, sentiment_text = sentiment_info.split(': ', 1)
                            figure = figure_sentiment.split(' ')[0]
                            sentiment = sentiment_text.split(' ')[0].strip('():')  # Strip colon from sentiment
                            data.append({'Outlet': outlet, 'Figure': figure, 'Sentiment': sentiment})
                        except ValueError:
                            print("Error splitting:", sentiment_info)  # Debugging print

    df = pd.DataFrame(data)
    if df.empty:
        print("No data processed.")
    else:
        print("Dataframe created:", df.head())  # Check the first few rows of the DataFrame
    return df

# Folder containing the files
folder_path = 'C:/Users/schma/Documents/GIT/PoliticalPolarisation/GPT_sentiment_data/'

# Initialize an empty list to store DataFrames
dfs = []

# Loop through files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):  # Process only text files
        # Extract the date (month and day) from the file name
        file_date = filename.split('_')[0]
        file_date += '_' + filename.split('_')[1]

        # Get the file path
        file_path = os.path.join(folder_path, filename)
        
        # Process headlines and get DataFrame
        df = process_headlines(file_path)
        
        # Add date column to the DataFrame
        df['Date'] = file_date
        
        # Append DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)

# Group by date and create separate pivot tables for each date
pivot_tables = []
for date, group in combined_df.groupby('Date'):
    pivot_table = pd.pivot_table(group, index=['Outlet', 'Figure'], columns='Sentiment', aggfunc='size', fill_value=0)
    pivot_table.reset_index(inplace=True)  # Reset index to flatten the DataFrame
    pivot_table['Date'] = date  # Add date column
    pivot_tables.append(pivot_table)

# Concatenate all pivot tables into one DataFrame
summary_table = pd.concat(pivot_tables, ignore_index=True)

# Save the pivot tables to a CSV file
output_csv = 'summary2_table.csv'
summary_table.to_csv(output_csv, index=False)

print("Summary tables saved to:", output_csv)
