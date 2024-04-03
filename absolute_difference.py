from mediadata import(
    get_headline_df,
    get_biden_trump_dataframes
)
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime
import pandas as pd

def get_headlines_over_dates(media_org: str, start: datetime.date, end: datetime.date):
    headlines = []
    current_date = start_date
    while current_date < end_date:

        try:
            headlines.append(get_headline_df(media_org, current_date))
        except: 
            pass

        current_date += datetime.timedelta(1)
        
    if len(headlines) == 0:
        return pd.DataFrame()
    return pd.concat(headlines)


def get_training_data():
    all_fox = get_headlines_over_dates('FOX', start_date, end_date)
    all_cnn = get_headlines_over_dates('CNN', start_date, end_date)
    all_abc = get_headlines_over_dates('abc', start_date, end_date)
    all_daily = get_headlines_over_dates('daily', start_date, end_date)
    all_nbc = get_headlines_over_dates('nbc', start_date, end_date)
    all_nypost = get_headlines_over_dates('nypost', start_date, end_date)
    all_skyus = get_headlines_over_dates('skyus', start_date, end_date)
    all_smh = get_headlines_over_dates('smh', start_date, end_date)

    total = pd.concat([all_fox, all_cnn, all_abc, all_daily, all_nbc,all_nypost, all_skyus, all_smh])

    biden, trump, both, neither = get_biden_trump_dataframes(total)
    both = both[['Headline']]

    # filter out super tuesday biases
    both['Headline'] = both['Headline'].apply(lambda x: x.lower().replace('super', ''))

    SIA = SentimentIntensityAnalyzer()
    both['Compound'] = both['Headline'].apply(lambda x: SIA.polarity_scores(x)['compound'])
    both_sorted = both.sort_values('Compound')
    negative_sample = both_sorted[both_sorted['Compound'] < -0.4]
    positive_sample = both_sorted[both_sorted['Compound'] > 0.4]

    negative_sample.to_csv('negative_political_training_data.csv', index=False, encoding='UTF8')
    positive_sample.to_csv('positive_political_training_data.csv', index=False, encoding='UTF8')



if __name__ == '__main__':
    pass

