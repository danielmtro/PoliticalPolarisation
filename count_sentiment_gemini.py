import pandas as pd
import glob
import os
from datetime import datetime

path = 'Gemini_Sentiment/headlines_csv/'
all_files = glob.glob(path + "*.csv")

# Get all dates from filenames to initialize dictionaries
all_dates = sorted({datetime.strptime(os.path.basename(f).split('_')[1], '%Y-%m-%d').date() for f in all_files})

# Initialize dictionaries with 'NA' for all dates
cnn_trump_means = {date: 'NA' for date in all_dates}
cnn_biden_means = {date: 'NA' for date in all_dates}
fox_trump_means = {date: 'NA' for date in all_dates}
fox_biden_means = {date: 'NA' for date in all_dates}
nbc_trump_means = {date: 'NA' for date in all_dates}
nbc_biden_means = {date: 'NA' for date in all_dates}

for filename in all_files:
    df = pd.read_csv(filename)
    date_str = os.path.basename(filename).split('_')[1]
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    grouped = df.groupby(['channel', 'target'])

    for (channel, target), group in grouped:
        if len(group) >= 5:
            mean_sentiment = group['sentiment_gemini'].mean()
            if channel == 'CNN':
                if target == 'Trump':
                    cnn_trump_means[date_obj] = mean_sentiment
                elif target == 'Biden':
                    cnn_biden_means[date_obj] = mean_sentiment
            elif channel == 'FOX':
                if target == 'Trump':
                    fox_trump_means[date_obj] = mean_sentiment
                elif target == 'Biden':
                    fox_biden_means[date_obj] = mean_sentiment
            elif channel == 'NBC':
                if target == 'Trump':
                    nbc_trump_means[date_obj] = mean_sentiment
                elif target == 'Biden':
                    nbc_biden_means[date_obj] = mean_sentiment

# Create DataFrame
data = {
    'cnn_trump_mean': list(cnn_trump_means.values()),
    'cnn_biden_mean': list(cnn_biden_means.values()),
    'fox_trump_mean': list(fox_trump_means.values()),
    'fox_biden_mean': list(fox_biden_means.values()),
    'nbc_trump_mean': list(nbc_trump_means.values()),
    'nbc_biden_mean': list(nbc_biden_means.values()),
    'date': all_dates  # Unified list of all dates
}

df = pd.DataFrame(data)
print(df)

import pandas as pd
import glob
import os
from datetime import datetime

path = 'Gemini_Sentiment/headlines_csv/'
all_files = glob.glob(path + "*.csv")

# Initialize dictionaries for sentiment sums and counts
sentiment_sums = {}
article_counts = {}

# Define columns
channels_targets = [
    ('CNN', 'Trump'), ('CNN', 'Biden'),
    ('FOX', 'Trump'), ('FOX', 'Biden'),
    ('NBC', 'Trump'), ('NBC', 'Biden')
]

# Initialize the sums and counts
for channel, target in channels_targets:
    sentiment_sums[(channel, target)] = 0
    article_counts[(channel, target)] = 0

# Process each file
for filename in all_files:
    date_str = os.path.basename(filename).split('_')[1]
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Exclude specific dates
    if date_obj in [datetime(2024, 3, 8).date(), datetime(2024, 3, 20).date(), datetime(2024, 3, 21).date(),
                    datetime(2024, 3, 22).date(), datetime(2024, 4, 16).date(), datetime(2024, 4, 17).date()]:
        continue

    df = pd.read_csv(filename)
    grouped = df.groupby(['channel', 'target'])

    # Accumulate sums and counts
    for (channel, target), group in grouped:
        sentiment_sums[(channel, target)] += group['sentiment_gemini'].sum()
        article_counts[(channel, target)] += len(group)

# Calculate weighted averages
weighted_averages = {}
for key in channels_targets:
    if article_counts[key] > 0:  # Avoid division by zero
        weighted_averages[key] = sentiment_sums[key] / article_counts[key]
    else:
        weighted_averages[key] = 'NA'  # Or use None, pd.NA, etc., depending on how you want to handle no data cases

# Output the results
for key, value in weighted_averages.items():
    print(f"{key}: {value}")
