from transformers import pipeline
import pandas as pd
from dataclasses import dataclass
import datetime
from tqdm import tqdm
tqdm.pandas()

@dataclass
class RedditPostData:
    CompanyRedditName : str
    PostTitle : str
    PostBody : str
    PostDate : datetime
    sentiment : str
    sentiment_score : float

# Load the sentiment analysis pipeline
sentiment_analysis = pipeline('sentiment-analysis')

# Data
texts = pd.read_csv('/Users/kirtanagopakumar/PycharmProjects/reddit_sentiment_analysis_trading_bot/reddit_scraper/reddit_data/CompanySubredditDataFull.csv')

# Get sentiment for each text
def get_sentiment(text):
    result = sentiment_analysis(text)[0]
    return result['label'], result['score']

texts['sentiment'], texts['sentiment_score'] = zip(*texts['PostTitle'].progress_apply(lambda x: get_sentiment(x)))

# Convert to CSV
texts.to_csv('/Users/kirtanagopakumar/PycharmProjects/reddit_sentiment_analysis_trading_bot/sentiment_analyser/sentiment_data/CompanySentimentDataFull.csv')

