import matplotlib.pyplot as plt
import pandas as pd
import datetime
from mediadata import get_headline_df, get_biden_trump_dataframes
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

def get_daily_vader_scores(media_org: str, date: datetime.date) -> tuple:
    """Gets the average VADER sentiment scores for Trump and Biden headlines for a given day."""
    df = get_headline_df(media_org, date)
    only_biden, only_trump, _, _ = get_biden_trump_dataframes(df)
    sid_obj = SentimentIntensityAnalyzer()
    
    biden_scores = [sid_obj.polarity_scores(headline)['compound'] for headline in only_biden['Headline']]
    trump_scores = [sid_obj.polarity_scores(headline)['compound'] for headline in only_trump['Headline']]
    
    biden_average = np.sum(biden_scores) if biden_scores else None
    trump_average = np.sum(trump_scores) if trump_scores else None
    
    return biden_average, trump_average

def plot_vader_scores_over_time(media_org: str, start_date: datetime.date, end_date: datetime.date, window_size: int = 1):
    """Plots the average VADER sentiment scores for Trump and Biden headlines over a range of dates, aggregated over a specified window size."""
    current_date = start_date
    biden_scores = []
    trump_scores = []
    dates = []

    while current_date <= end_date:
        biden_window_scores = []
        trump_window_scores = []
        for i in range(window_size):
            if current_date + datetime.timedelta(days=i) > end_date:
                break
            try:
                biden_score, trump_score = get_daily_vader_scores(media_org, current_date + datetime.timedelta(days=i))
                if biden_score is not None:
                    biden_window_scores.append(biden_score)
                if trump_score is not None:
                    trump_window_scores.append(trump_score)
            except KeyError:
                print(f"No data for {media_org} on {(current_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d')}")

        if biden_window_scores and trump_window_scores:
            biden_scores.append(np.sum(biden_window_scores))
            trump_scores.append(np.sum(trump_window_scores))
            dates.append(current_date)
        
        current_date += datetime.timedelta(days=window_size)

    plt.figure(figsize=(12, 6))
    plt.plot(dates, biden_scores, marker='o', label='Biden')
    plt.plot(dates, trump_scores, marker='o', label='Trump')
    plt.xlabel('Date')
    plt.ylabel('Average VADER Sentiment Score')
    plt.title(f'Average VADER Sentiment Score Over Time for {media_org}')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    start_date = datetime.date(2024, 3, 8)
    end_date = datetime.date(2024, 3, 8)
    plot_vader_scores_over_time('CNN', start_date, end_date, window_size=3)

if __name__ == '__main__':
    start_date = datetime.date(2024, 3, 8)
    end_date = datetime.date(2024, 3, 8)
    plot_vader_scores_over_time('FOX', start_date, end_date, window_size=3)
