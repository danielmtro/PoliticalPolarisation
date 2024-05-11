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
                            if sentiment != 'mixed':  # Ignore 'mixed' sentiment
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

# Group by date, outlet, and figure, and calculate the mean sentiment score
grouped_df = combined_df.groupby(['Date', 'Outlet', 'Figure', 'Sentiment']).size().unstack(fill_value=0).reset_index()
grouped_df['Sentiment_Numeric'] = grouped_df['Positive'].astype(int) - grouped_df['Negative'].astype(int)

# Read the data from the CSV file
df = pd.read_csv("summary_table_with_means.csv")

# Calculate the mean sentiment score
df['Mean_Sentiment'] = df['Sentiment_Numeric'] / (df['Negative'] + df['Neutral'] + df['Positive'])

# Write the updated data back to the CSV file
df.to_csv("summary_table_with_means.csv", index=False)

import pandas as pd

# Read the data from the CSV file
df = pd.read_csv("summary_table_with_means.csv")

# Define exclusion dates
exclusion_dates = ['March_8', 'March_20', 'March_21', 'March_22', 'April_16', 'April_17']

# Filter the DataFrame to exclude specified dates
filtered_df = df[~df['Date'].isin(exclusion_dates)]

# Initialize lists to store average sentiments
average_sentiments = []

# Loop through each row in the DataFrame
for index, row in filtered_df.iterrows():
    # Filter the DataFrame for the current combination of outlet and figure
    subset_df = filtered_df[(filtered_df['Outlet'] == row['Outlet']) & (filtered_df['Figure'] == row['Figure'])]
    
    # Calculate the total number of articles
    total_articles = subset_df['Negative'] + subset_df['Neutral'] + subset_df['Positive']
    total_articles_sum = total_articles.sum()
    
    # Calculate the sum of Sentiment_Numerics
    sentiment_numerics_sum = subset_df['Sentiment_Numeric'].sum()
    
    # Calculate the average sentiment
    if total_articles_sum != 0:
        average_sentiment = sentiment_numerics_sum / total_articles_sum
    else:
        average_sentiment = 0
    
    # Append the average sentiment to the list
    average_sentiments.append(average_sentiment)

# Add the average sentiments as new columns in the DataFrame
filtered_df['Average_Sentiment'] = average_sentiments

# Write the updated data back to the CSV file
filtered_df.to_csv("summary_table_with_means.csv", index=False)


import matplotlib.pyplot as plt
import pandas as pd
import datetime
from mediadata import get_headline_df, get_unique_headlines

def get_headline_counts(media_org: str, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """Get the count of unique headlines for each day between start_date and end_date for a specific media organization."""
    current_date = start_date
    headlines_counts = []
    days = []

    while current_date <= end_date:
        try:
            headlines = get_unique_headlines(media_org, current_date)
            headlines_count = len(headlines)
        except KeyError:
            headlines_count = 0  # If no headlines found, count is zero
        
        headlines_counts.append(headlines_count)
        days.append(current_date)
        current_date += datetime.timedelta(days=1)

    df = pd.DataFrame({
        'Date': days,
        'Headline Totals': headlines_counts
    })
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

# Example usage
start_date = datetime.date(2024, 3, 3)
end_date = datetime.date(2024, 4, 24)
CNN_headlines = get_headline_counts('CNN', start_date, end_date)
FOX_headlines = get_headline_counts('FOX', start_date, end_date)
NBC_headlines = get_headline_counts('NBC', start_date, end_date)

# List of specific dates you want to filter on
specific_dates = ['2024-04-05', '2024-04-07', '2024-04-12', '2024-04-16', '2024-04-17', '2024-03-05', '2024-03-08', '2024-03-16', '2024-03-21', '2024-03-14', '2024-03-16', '2024-03-17', '2024-03-27']
specific_dates = pd.to_datetime(specific_dates)

# Filter CNN_headlines DataFrame to only include specific dates
filtered_CNN_df = CNN_headlines[CNN_headlines.index.isin(specific_dates)]


# Filter CNN_headlines DataFrame to only include specific dates
filtered_FOX_df = FOX_headlines[FOX_headlines.index.isin(specific_dates)]

# Filter CNN_headlines DataFrame to only include specific dates
filtered_NBC_df = NBC_headlines[NBC_headlines.index.isin(specific_dates)]

print(filtered_CNN_df)
print(filtered_FOX_df)
print(filtered_NBC_df)

# Assuming filtered_CNN_df, filtered_FOX_df, filtered_NBC_df are already defined and filtered
#combined_df = pd.concat([filtered_CNN_df, filtered_FOX_df, filtered_NBC_df], axis=1, keys=['CNN', 'FOX', 'NBC'])

# Rename columns to make them more descriptive
#combined_df.columns = ['CNN Headline Totals', 'FOX Headline Totals', 'NBC Headline Totals']

#import pandas as pd

# Assuming combined_df is already defined
# Convert the Date index to the desired format
#combined_df.index = combined_df.index.strftime('%B_%d')

# Convert the formatted date strings to lowercase
#combined_df.index = combined_df.index.str.lower()

# Remove leading zeros from the day if the day is a single digit
#combined_df.index = combined_df.index.str.replace('_0', '_', regex=True)

# Now your DataFrame's index is correctly formatted, you can proceed to save it
#combined_df.to_csv('filtered_headline_totals.csv')

# Export to CSV
#combined_df.to_csv('filtered_headline_totals.csv')
