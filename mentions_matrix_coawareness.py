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

def check_mentions(headlines: list, target_orgs: list) -> int:
    """ Count how many times target organizations are mentioned in the headlines. """
    mention_count = 0
    for headline in headlines:
        for org in target_orgs:
            if org in headline:
                mention_count += 1
                break  # Exit the inner loop once a mention is found
    return mention_count

def get_daily_mentions(media_org: str, date: datetime.date) -> pd.DataFrame:
    """ Retrieve headlines and check for mentions of other organizations. """
    df = get_headline_df(media_org, date)
    headlines = df['Headline'].tolist()
    mentions = {}
    orgs = ['CNN', 'FOX', 'NBC']
    if media_org == 'NBC':
        target_org = 'MSNBC'
    else:
        target_org = media_org

    for org in orgs:
        if org != target_org:
            mentions[org] = check_mentions(headlines, [org])
    
    return mentions

def build_adjacency_matrix(date: datetime.date):
    """ Build an adjacency matrix for mentions on a specific date. """
    orgs = ['CNN', 'FOX', 'NBC']
    matrix = np.zeros((3, 3), dtype=int)
    
    for i, org in enumerate(orgs):
        mentions = get_daily_mentions(org, date)
        for j, target_org in enumerate(orgs):
            if org != target_org:
                matrix[i][j] = mentions.get(target_org, 0)
    
    return matrix

import numpy as np

def invert_matrix(matrix):
    """ Attempt to invert a matrix. """
    try:
        # Compute the determinant to check if the matrix is invertible
        if np.linalg.det(matrix) == 0:
            return "Matrix is singular and cannot be inverted."
        else:
            # Invert the matrix
            inverted_matrix = np.linalg.inv(matrix)
            return inverted_matrix
    except np.linalg.LinAlgError:
        return "An error occurred during matrix inversion."

# Example usage with your adjacency matrix
date = datetime.date(2024, 3, 16)
adjacency_matrix = build_adjacency_matrix(date)


def plot_adjacency_matrix(matrix, labels):
    """Plot the adjacency matrix as a heatmap with labels."""
    fig, ax = plt.subplots()
    cax = ax.matshow(matrix.T, cmap='coolwarm')  # Transpose the matrix
    
    # Set axis properties
    plt.xticks(np.arange(len(labels)), labels)
    plt.yticks(np.arange(len(labels)), labels)
    plt.xlabel('Mentioned By')
    plt.ylabel('Mentions')
    
    # Add colorbar to the heatmap
    fig.colorbar(cax)
    
    # Adding values on the heatmap
    for (i, j), val in np.ndenumerate(matrix.T):  # Transpose the matrix
        ax.text(j, i, f'{val}', ha='center', va='center', color='black')

    plt.show()
    

# Example labels
media_orgs = ['CNN', 'FOX', 'NBC']

# Plot the matrix
plot_adjacency_matrix(adjacency_matrix, media_orgs)

