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
from mediadata import get_headline_df

def get_lib_labor_dataframes(df: pd.DataFrame) -> Tuple[pd.DataFrame]:
    """Gets a dataframe where we have headlines that only mention Liberal/Dutton, Labor/Albanese, both and none"""
    headline = df.columns[0]
    original_columns = df.columns
    
    df['contains_labor_albanese'] = df[headline].apply(lambda x: True if ('labor' or 'albanese') in x.lower() else False)
    df['contains_liberal_dutton'] = df[headline].apply(lambda x: True if ('liberal' or 'dutton') in x.lower() else False)
    df['contains_both'] = df.apply(lambda row: row['contains_labor_albanese'] and row['contains_liberal_dutton'], axis=1)

    # separate into two unique dataframes that are only referencing biden and only referencing trump
    only_labor_albanese = df[df['contains_labor_albanese'] & ~df['contains_both']][original_columns]
    only_liberal_dutton = df[df['contains_liberal_dutton'] & ~df['contains_both']][original_columns]
    both = df[df['contains_both']]
    neither = df[~df['contains_both']]
    
    return only_labor_albanese, only_liberal_dutton, both, neither

def get_raw_counts(media_org: str, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """Get the percentage of Albanese/Labor (left) and Dutton/Biden (right) headlines for each day."""
    current_date = start_date
    left_counts = []
    right_counts = []
    right_left_counts = []
    days = []

    while current_date <= end_date:

        try: 
            df = get_headline_df(media_org, current_date)
        except:
            current_date += datetime.timedelta(days=1)
            continue

        only_labor_albanese, only_liberal_dutton, both, _ = get_lib_labor_dataframes(df)
        total_headlines = len(df)

        if total_headlines > 0:
            left_count = len(only_labor_albanese)
            right_count = len(only_liberal_dutton)
            right_left_count = len(both)
        else:
            left_count = 0
            right_count = 0
            right_left_count = len(both)

        left_counts.append(left_count)
        right_counts.append(right_count)
        right_left_counts.append(right_left_count)
        days.append(current_date)

        current_date += datetime.timedelta(days=1)

    df = pd.DataFrame()
    df['Date'] = days
    df['Labor/Albanese'] = left_counts
    df['Liberal/Dutton'] = right_counts
    df['Labor/Albanese and Liberal/Dutton'] = right_left_counts
    df.set_index('Date')

    return df

start_date = datetime.date(2024, 3, 4)
end_date = datetime.date(2024, 4, 18)

index=["Labor/Albanese", "Liberal/Dutton", "Labor/Albanese and Liberal/Dutton"]
smh_df = get_raw_counts('smh', start_date, end_date)
ABC_AU_df = get_raw_counts('abcau', start_date, end_date)

smh_df.plot(x = 'Date', kind='bar', stacked=True,figsize=(15, 8))
plt.title('Sydney Morning Herald Mentions of Albanese/Labor and Dutton/Liberal over Time')
plt.ylabel('Raw Counts')
plt.xlabel('Dates')
plt.show()

ABC_AU_df.plot(x = 'Date', kind='bar', stacked=True,figsize=(15, 8))
plt.title('ABC AU Mentions of Albanese/Labor and Dutton/Liberal over Time')
plt.ylabel('Raw Counts')
plt.xlabel('Dates')
plt.show()