import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import glob
import os
import datetime
from typing import List, Tuple
from mediadata import get_headline_df, get_biden_trump_dataframes

def get_headlines(media_org: str, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """Collect headlines for Biden, Trump, and both from each day."""
    current_date = start_date
    biden_headlines = []
    trump_headlines = []
    days = []

    while current_date <= end_date:
        try: 
            df = get_headline_df(media_org, current_date)
            only_biden, only_trump, _ , _ = get_biden_trump_dataframes(df)
        except:
            # Move to the next day if there's an error (e.g., no data available for that day)
            current_date += datetime.timedelta(days=1)
            continue

        # Append headlines or a placeholder if none
        biden_headlines.append(list(only_biden['Headline']) if not only_biden.empty else ['No Biden headlines'])
        trump_headlines.append(list(only_trump['Headline']) if not only_trump.empty else ['No Trump headlines'])

        days.append(current_date)
        current_date += datetime.timedelta(days=1)

    # Create a DataFrame to store the results
    df = pd.DataFrame({
        'Date': days,
        'Media Org': [media_org] * len(days),  # Add media organization identifier
        'Biden Headlines': biden_headlines,
        'Trump Headlines': trump_headlines,
    })

    return df

start_date = datetime.date(2024, 4, 10)
end_date = datetime.date(2024, 4, 10)

# Retrieve headlines data frames
CNN_headlines_df = get_headlines('CNN', start_date, end_date)
FOX_headlines_df = get_headlines('FOX', start_date, end_date)
NBC_headlines_df = get_headlines('NBC', start_date, end_date)

start_date_str = start_date.strftime("%Y-%m-%d")

# Combine data frames
combined_df = pd.concat([CNN_headlines_df, FOX_headlines_df, NBC_headlines_df])


output_path = f'C:/Users/schma/Documents/GIT/PoliticalPolarisation/Combined_Headlines_{start_date_str}_Output.csv'

input_csv_path = f'C:/Users/schma/Documents/GIT/PoliticalPolarisation/Combined_Headlines_{start_date_str}_Output.csv'
output_txt_path = f'C:/Users/schma/Documents/GIT/PoliticalPolarisation/headline_txts_by_day_and_org/Headlines_{start_date_str}_Output.txt'


combined_df.to_csv(output_path, encoding='utf-8', index=False)

import pandas as pd
import re

def csv_to_txt_with_split_lines(input_csv_path, output_txt_path):
    try:
        # Read the CSV file using the correct encoding
        df = pd.read_csv(input_csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        # If UTF-8 encoding fails, try 'ISO-8859-1' instead
        df = pd.read_csv(input_csv_path, encoding='ISO-8859-1')

    # Open the output text file with UTF-8 encoding
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        # Iterate over each row in the dataframe
        for index, row in df.iterrows():
            # Get the media organization for this row
            media_org = row['Media Org'] if 'Media Org' in df.columns else "Unknown"
            
            # Process each of the headline columns
            for category in ['Biden', 'Trump', 'Both']:
                column_name = f"{category} Headlines"
                # Check if the column exists and is not empty
                if column_name in df.columns and pd.notna(row[column_name]):
                    # Skip the placeholder text indicating no headlines
                    if row[column_name] not in ["['No headlines for both']", '["No headlines for both"]']:
                        # Use regex to find all the headlines
                        headlines = re.findall(r"['\"](.*?)['\"](?=\s*,\s*['\"]|$)", row[column_name])
                        for line in headlines:
                            # Skip empty lines or placeholders
                            if line and not line.startswith("No "):
                                # Write the media organization, category, and the headline to the file
                                f.write(f"{media_org} - {category}: {line}\n")


# Run the function
csv_to_txt_with_split_lines(input_csv_path, output_txt_path)
# Delete the CSV file after the text file is created
os.remove(output_path)