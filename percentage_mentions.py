import matplotlib.pyplot as plt
import pandas as pd
import datetime
from mediadata import get_headline_df, get_biden_trump_dataframes

def get_headline_percentages(media_org: str, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """Get the percentage of Biden and Trump headlines for each day."""
    current_date = start_date
    biden_percentages = []
    trump_percentages = []
    days = []

    while current_date <= end_date:

        try: 
            df = get_headline_df(media_org, current_date)
        except:
            current_date += datetime.timedelta(days=1)
            continue

        only_biden, only_trump, _, _ = get_biden_trump_dataframes(df)
        total_headlines = len(df)

        if total_headlines > 0:
            biden_percentage = len(only_biden) / total_headlines * 100
            trump_percentage = len(only_trump) / total_headlines * 100
        else:
            biden_percentage = 0
            trump_percentage = 0

        biden_percentages.append(biden_percentage)
        trump_percentages.append(trump_percentage)
        days.append(current_date)

        current_date += datetime.timedelta(days=1)

    df = pd.DataFrame()
    df['Date'] = days
    df['Biden'] = biden_percentages
    df['Trump'] = trump_percentages
    #df['Total'] = df.apply(lambda row: row['Biden'] + row['Trump'], axis=1)
    df['Total'] = df['Biden'] + df['Trump']
    df.set_index('Date')

    return df


start_date = datetime.date(2024, 3, 4)
end_date = datetime.date(2024, 4, 25)

CNN_df = get_headline_percentages('CNN', start_date, end_date)
FOX_df = get_headline_percentages('FOX', start_date, end_date)
#ABC_US_df = get_headline_percentages('abcus', start_date, end_date)
#NBC_df = get_headline_percentages('nbc', start_date, end_date)
