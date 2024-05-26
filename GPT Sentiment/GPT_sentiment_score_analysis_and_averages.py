import os
import pandas as pd

# Processing GPT headline data – this can be found in the GPT_sentiment_data folder in the Github

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
                            
                            # Exclude 'Mixed' sentiment
                            if sentiment != 'Mixed':
                                data.append({'Outlet': outlet, 'Figure': figure, 'Sentiment': sentiment})
                        except ValueError:
                            print("Error splitting:", sentiment_info)  # Debugging print statement

    df = pd.DataFrame(data)
    if df.empty:
        print("No data processed.")
    else:
        print("Dataframe created:", df.head())  # Check the first few rows of the DataFrame
    return df

# Folder containing the files – adjust as needed
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

# Total counts calculated using the mediadata file – outputs adjusted to accommodate for the fact that there some days don’t have political headlines in the values
total_counts_list = [234, 234, 656, 656, 176, 176, # April 12 - CNN, FOX, NBC
                                     176, 656, 656, 205, 205, # April 16
                                     190, 670, 670, 190, 190, # April 17
                                     171, 171, 675, 675, 171, 171, # April 5
                                     153, 153, 364, 364, 117, 117, # April 7
                                     109, 109, 447, 447, 103, 103, # March 14
                                     176, 176, 569, 569, 196, 196, # March 16
                                     103, 103, 447, 447, 217, 217, # March 17
                                     196, 196, 657, 657, 692, 692, # March 21
                                     167, 167, 600, 600, 217, 217, #March 27
                                     263, 263, 692, 692, 217, 217] # March 8 

# Add total counts as a column to the DataFrame
summary_table['Total_Counts'] = total_counts_list

# Add positive and negative percentage columns
summary_table['Positive_Percentage'] = summary_table['Positive'] / summary_table['Total_Counts'] * 100
summary_table['Negative_Percentage'] = summary_table['Negative'] / summary_table['Total_Counts'] * 100

# Save the pivot tables to a CSV file
output_csv = 'positive_negative_GPT_analysis.csv'
summary_table.to_csv(output_csv, index=False)

print("Summary tables saved to:", output_csv)

import pandas as pd

# Read the data from the CSV file
df = pd.read_csv(‘positive_negative_GPT_analysis.csv')

# Filter out specific dates of events to exclude from BAU average
dates_to_exclude = ['march_8', 'march_21', 'april_16']
df = df[~df['Date'].isin(dates_to_exclude)]

# Group the data by 'Outlet' and 'Figure' to calculate the statistics
grouped_df = df.groupby(['Outlet', 'Figure'])

# Calculate weighted averages and standard deviations for Percentage Positive
weighted_avg_pos = grouped_df.apply(lambda x: ((x['Positive'] / x['Totals']) * 100).mean())
std_dev_pos = grouped_df.apply(lambda x: ((x['Positive'] / x['Totals']) * 100).std())
weighted_avg_pos = weighted_avg_pos.reset_index()
std_dev_pos = std_dev_pos.reset_index()

# Rename columns appropriately
weighted_avg_pos.rename(columns={0: 'Weighted Avg Positive'}, inplace=True)
std_dev_pos.rename(columns={0: 'Std Dev Positive'}, inplace=True)

# Merge weighted averages and standard deviations for positive sentiments
result_pos = pd.merge(weighted_avg_pos, std_dev_pos, on=['Outlet', 'Figure'])

# Calculate weighted averages and standard deviations for Percentage Negative
weighted_avg_neg = grouped_df.apply(lambda x: ((x['Negative'] / x['Totals']) * 100).mean())
std_dev_neg = grouped_df.apply(lambda x: ((x['Negative'] / x['Totals']) * 100).std())
weighted_avg_neg = weighted_avg_neg.reset_index()
std_dev_neg = std_dev_neg.reset_index()

# Rename columns appropriately
weighted_avg_neg.rename(columns={0: 'Weighted Avg Negative'}, inplace=True)
std_dev_neg.rename(columns={0: 'Std Dev Negative'}, inplace=True)

# Merge weighted averages and standard deviations for negative sentiments
result_neg = pd.merge(weighted_avg_neg, std_dev_neg, on=['Outlet', 'Figure'])

# Define the file name for the output CSV
output_file = 'weighted_avg_std_dev_results.csv'

# Write the results to a new CSV file
with open(output_file, 'w') as f:
    # Write results for positive sentiments
    f.write("Results with Weighted Averages and Standard Deviations for Percentage Positive:\n")
    result_pos.to_csv(f, index=False)
    f.write("\n")
    # Write results for negative sentiments
    f.write("Results with Weighted Averages and Standard Deviations for Percentage Negative:\n")
    result_neg.to_csv(f, index=False)

print("Results have been written to:", output_file)



