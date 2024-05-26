import matplotlib.pyplot as plt
import pandas as pd
from typing import List
from collections import defaultdict
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



def get_headline_percentages(media_orgs: List[str], start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:


    output = defaultdict(list)
    current_date = start_date 
    while current_date <= end_date:

        try: 

            for media_org in media_orgs:
                df = get_headline_df(media_org, current_date)

                num_political = len([1 for i in df['Headline'] if ('biden' in i.lower() or 'trump' in i.lower())])
                percentage= num_political/len(df)
                output[media_org].append(percentage)

            output['Date'].append(pd.to_datetime(current_date))
            current_date += datetime.timedelta(days=1)


        except:
            current_date += datetime.timedelta(days=1)
            continue
    
    return pd.DataFrame(output).set_index('Date')

