import datetime
import pandas as pd
from collections import defaultdict
from typing import List
from mediadata import get_headline_df, get_biden_trump_dataframes, get_accumulated_headlines
from nltk.corpus import stopwords


def remove_stopwords(df: pd.DataFrame, column = 'Headline') -> pd.DataFrame:
    """Removes the stopwords from the Headline column of a dataframe"""
    set_stopwords = set(stopwords.words('English'))
    df_no_stopwords = df.copy()
    df_no_stopwords[column] = df_no_stopwords[column].apply(lambda x: ' '.join([i for i in x.split() if i not in set_stopwords]))
    return df_no_stopwords


def build_documents(df: pd.DataFrame):
    """Builds documents based off dataframe containing different values in the MediaOrg column"""
    documents = []
    all_media_orgs = list(set(df['MediaOrg']))
    for org in all_media_orgs:
        sub_df = df[df['MediaOrg'] == org]
        sub_df_document = ' '.join(list(sub_df['Headline']))
        documents.append(sub_df_document)
    return documents, all_media_orgs


def get_tf_idf_df(documents, labels):
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectoriser = TfidfVectorizer()
    vectors = vectoriser.fit_transform(documents)
    feature_names = vectoriser.get_feature_names_out()
    dense = vectors.todense()
    denselist = dense.tolist()
    tf_idf_df = pd.DataFrame(denselist, columns=feature_names)
    tf_idf_df.index = labels
    return tf_idf_df[[i for i in tf_idf_df.columns if not i.isnumeric()]].T


if __name__ == '__main__':
    start_date = datetime.date(2024, 3, 18)
    end_date = datetime.date(2024, 3, 21)
    media_orgs = ['FOX', 'CNN']

    # get a dataframe of all the media organisations around the court day
    df = get_accumulated_headlines(start_date, end_date, media_orgs)
    df_no_stopwords = remove_stopwords(df)

    biden, trump, _, _ = get_biden_trump_dataframes(df_no_stopwords)

    documents, labels = build_documents(biden)
    tf_idf_df = get_tf_idf_df(documents, labels)