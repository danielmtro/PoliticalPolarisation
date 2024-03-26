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


def get_unique_headlines(media_org: str, date: datetime.date, folder: str = 'logs',):
    """Gets a set of unique headlines from a media organisation"""
    
    day = date.day
    month = date.month
    year = date.year
    
    if day < 10:
        day = f'0{day}'
    if month < 10:
        month = f'0{month}'

    unique_headlines = set()
    for filename in glob.glob(f'{folder}\\LOG_{media_org}_{day}_{month}_{year}' +'_*.txt'):
        f = open(filename,encoding="utf-8")
        data = f.read()
        lines = data.splitlines()
        for line in lines:
            unique_headlines.add(line)
            
    if len(unique_headlines) == 0:
        raise KeyError("No data on the date you provided")

    return unique_headlines


def get_headline_df(media_org: str, date: datetime.date) -> pd.DataFrame:
    unique_headlines = get_unique_headlines(media_org, date)
    return pd.DataFrame({'Headline': list(unique_headlines)})


def embed_data(df: pd.DataFrame, model = SentenceTransformer('all-MiniLM-L6-v2')) -> pd.DataFrame:
    """Embeds a dataframe into the LLM space""" 
    # generalise function to allow any dataframe columns
    column_head = df.columns[0]
    # convert text into embeddings
    embeddings = df[column_head].map(lambda x: model.encode(x))

    #converts embeddings into a dataframe
    embeddings = embeddings.to_frame()
    embeddings = embeddings[column_head].apply(pd.Series)
    return embeddings


def embed_point(sentence: str, model=SentenceTransformer('all-MiniLM-L6-v2')) -> np.array:
    """Embeds a single sentence or string in the model"""
    encoded_value = model.encode(sentence)
    return encoded_value


def get_biden_trump_dataframes(df: pd.DataFrame) -> Tuple[pd.DataFrame]:
    """Gets a dataframe where we have headlines that only mention biden, only trump, both and none"""
    headline = df.columns[0]
    
    df['contains_biden'] = df[headline].apply(lambda x: True if 'biden' in x.lower() else False)
    df['contains_trump'] = df[headline].apply(lambda x: True if 'trump' in x.lower() else False)
    df['contains_both'] = df.apply(lambda row: row['contains_biden'] and row['contains_trump'], axis=1)

    # separate into two unique dataframes that are only referencing biden and only referencing trump
    only_biden = df[df['contains_biden'] & ~df['contains_both']][['Headline']]
    only_trump = df[df['contains_trump'] & ~df['contains_both']][['Headline']]
    both = df[df['contains_both']]
    neither = df[~df['contains_both']]
    
    return only_biden, only_trump, both, neither


def get_daily_polarisation(media_org: str, date: datetime.date) -> float:
    """Gets the cosine similarity between all biden articles and all trump articles for a given day."""
    df = get_headline_df(media_org, date)
    only_biden, only_trump, _, _ = get_biden_trump_dataframes(df)

    # aggregate all the headlines into one string (each headline separated by a fullstop)
    aggregated_biden = '. '.join(only_biden['Headline'])
    aggregated_trump = '. '.join(only_trump['Headline'])
    
    # embed resultant headlines in the model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    biden_encoded = embed_point(aggregated_biden, model)
    trump_encoded = embed_point(aggregated_trump, model)
    
    # determine cosine similarity - 2D array output
    similarity = cosine_similarity([biden_encoded], [trump_encoded])
    
    return similarity[0][0]


def get_media_organisation_polarisation_df(media_org: str,
                                           start_date: datetime.date,
                                           end_date: datetime.date,
                                           log_failures=False):
    """Gets a dataframe containing the polarisation between biden and trump sentiment for a media organisation over time."""
    current_date = start_date
    polarisation_vals = []
    polarisation_dates = []
    while current_date <= end_date:

        try:
            polarisation = get_daily_polarisation(media_org, current_date)
            polarisation_vals.append(polarisation)
            polarisation_dates.append(current_date)
        except KeyError:

            if log_failures:
                print(f"No data on {current_date.strftime('%d %b %Y')}")

        current_date += datetime.timedelta(1)

    datetime_list = [datetime.datetime(date.year, date.month, date.day) for date in polarisation_dates]
    df = pd.DataFrame({"Date": datetime_list, f"{media_org}": polarisation_vals}).set_index('Date')

    return df


if __name__ == '__main__':

    # test the implementation with some sample dates
    start_date = datetime.date(2024, 3, 1)
    end_date = datetime.date(2024, 3, 9)

    combined_df = pd.DataFrame()
    cnn_df = get_media_organisation_polarisation_df('CNN', start_date, end_date)
    fox_df = get_media_organisation_polarisation_df('FOX', start_date, end_date)

    combined_df['CNN'] = cnn_df
    combined_df['FOX'] = fox_df

    fig, ax = plt.subplots()
    combined_df.plot(ax=ax)
    ax.set_ylabel('Polarisation')
    ax.set_title('Different Media Organisations Polarisation')
    ax.set_facecolor("#ffffff")
    ax.grid(axis="y", which="major", color="#666666", linestyle='--', alpha=0.4)