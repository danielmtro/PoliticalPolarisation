from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from mediadata import get_headline_df, get_biden_trump_dataframes
import numpy as np

def get_daily_textblob_scores_and_errors(media_org: str, date: datetime.date) -> tuple:
    """Gets the average TextBlob sentiment scores and errors for Trump and Biden headlines for a given day."""
    df = get_headline_df(media_org, date)
    only_biden, only_trump, _, _ = get_biden_trump_dataframes(df)
    
    biden_scores = []
    biden_errors = []
    for headline in only_biden['Headline']:
        analysis = TextBlob(headline)
        biden_scores.append(analysis.sentiment.polarity)
        biden_errors.append((analysis.sentiment.subjectivity))
    
    trump_scores = []
    trump_errors = []
    for headline in only_trump['Headline']:
        analysis = TextBlob(headline)
        trump_scores.append(analysis.sentiment.polarity)
        trump_errors.append((analysis.sentiment.subjectivity))
    
    biden_average = np.mean(biden_scores) if biden_scores else None
    trump_average = np.mean(trump_scores) if trump_scores else None
    biden_error = np.mean(biden_errors) if biden_errors else None
    trump_error = np.mean(trump_errors) if trump_errors else None
    
    return (biden_average, trump_average), (biden_error, trump_error)

def plot_textblob_scores_over_time_with_errors(media_org: str, start_date: datetime.date, end_date: datetime.date, window_size: int = 1):
    """Plots the average TextBlob sentiment scores with error bars for Trump and Biden headlines over a range of dates, aggregated over a specified window size."""
    current_date = start_date
    biden_scores = []
    trump_scores = []
    biden_errors = []
    trump_errors = []
    dates = []

    while current_date <= end_date:
        biden_window_scores = []
        trump_window_scores = []
        biden_window_errors = []
        trump_window_errors = []
        for i in range(window_size):
            if current_date + datetime.timedelta(days=i) > end_date:
                break
            try:
                (biden_score, trump_score), (biden_error, trump_error) = get_daily_textblob_scores_and_errors(media_org, current_date + datetime.timedelta(days=i))
                if biden_score is not None:
                    biden_window_scores.append(biden_score)
                    biden_window_errors.append(biden_error)
                if trump_score is not None:
                    trump_window_scores.append(trump_score)
                    trump_window_errors.append(trump_error)
            except KeyError:
                print(f"No data for {media_org} on {(current_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d')}")

        if biden_window_scores and trump_window_scores:
            biden_scores.append(np.mean(biden_window_scores))
            trump_scores.append(np.mean(trump_window_scores))
            biden_errors.append(np.mean(biden_window_errors))
            trump_errors.append(np.mean(trump_window_errors))
            dates.append(current_date)
        
        current_date += datetime.timedelta(days=window_size)

    plt.figure(figsize=(12, 6))
    plt.errorbar(dates, biden_scores, yerr=biden_errors, marker='o', label='Biden', capsize=5)
    plt.errorbar(dates, trump_scores, yerr=trump_errors, marker='o', label='Trump', capsize=5)
    plt.xlabel('Date')
    plt.ylabel('Average TextBlob Sentiment Score')
    plt.title(f'Average TextBlob Sentiment Score Over Time for {media_org} with Error Bars')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    start_date = datetime.date(2024, 3, 1)
    end_date = datetime.date(2024, 3, 25)
    plot_textblob_scores_over_time_with_errors('CNN', start_date, end_date, window_size=1)
    plot_textblob_scores_over_time_with_errors('FOX', start_date, end_date, window_size=1)
