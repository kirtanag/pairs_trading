import pandas as pd
import numpy as np

df_sentiment = pd.read_csv('/Users/kirtanagopakumar/PycharmProjects/reddit_sentiment_analysis_trading_bot/sentiment_analyser/sentiment_data/CompanySentimentDataFull.csv')
print(df_sentiment['sentiment'].value_counts())


# Check for NA values
print(f'NA values in {len(df_sentiment[df_sentiment["sentiment_score"].isna()])}')

