import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import glob
import os
import datetime
from typing import List, Tuple
from sentence_transformers import SentenceTransformer 
from sklearn.metrics.pairwise import cosine_similarity
from mediadata import get_headline_df, get_biden_trump_dataframes


def get_raw_counts(media_org: str, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """Get the percentage of Biden and Trump headlines for each day."""
    current_date = start_date
    biden_counts = []
    trump_counts = []
    biden_trump_counts = []
    days = []

    while current_date <= end_date:

        try: 
            df = get_headline_df(media_org, current_date)
        except:
            current_date += datetime.timedelta(days=1)
            continue

        only_biden, only_trump, both, _ = get_biden_trump_dataframes(df)
        total_headlines = len(df)

        if total_headlines > 0:
            biden_count = len(only_biden)
            trump_count = len(only_trump)
            biden_trump_count = len(both)
        else:
            biden_count = 0
            trump_count = 0
            biden_trump_count = len(both)

        biden_counts.append(biden_count)
        trump_counts.append(trump_count)
        biden_trump_counts.append(biden_trump_count)
        days.append(current_date)

        current_date += datetime.timedelta(days=1)

    df = pd.DataFrame()
    df['Date'] = days
    df['Biden'] = biden_counts
    df['Trump'] = trump_counts
    df['Biden and Trump'] = biden_trump_counts
    df.set_index('Date')

    return df

start_date = datetime.date(2024, 3, 4)
end_date = datetime.date(2024, 4, 18)

index=["Biden", "Trump", "Biden and Trump"]
CNN_df = get_raw_counts('CNN', start_date, end_date)
FOX_df = get_raw_counts('FOX', start_date, end_date)
NBC_df = get_raw_counts('NBC', start_date, end_date)

NBC_df.plot(x = 'Date', kind='bar', stacked=True,figsize=(15, 8))
plt.title('MSNBC Mentions of Trump and Biden over Time')
plt.ylabel('Raw Counts')
plt.xlabel('Dates')
plt.show()

FOX_df.plot(x = 'Date', kind='bar', stacked=True,figsize=(15, 8))
plt.title('FOX Mentions of Trump and Biden over Time')
plt.ylabel('Raw Counts')
plt.xlabel('Dates')
plt.show()

CNN_df.plot(x = 'Date', kind='bar', stacked=True,figsize=(15, 8))
plt.title('CNN Mentions of Trump and Biden over Time')
plt.ylabel('Raw Counts')
plt.xlabel('Dates')
plt.show()