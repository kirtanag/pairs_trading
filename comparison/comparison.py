import pandas as pd
import datetime
import numpy as np

sentiment_df = pd.read_csv('/Users/kirtanagopakumar/PycharmProjects/reddit_sentiment_analysis_trading_bot/sentiment_analyser/sentiment_data/CompanySentimentDataFull.csv')

# Since Reddit reviews tend to be overwhelmingly negative, let's set a high confidence rate only above which a negative review is considered truly negative
def rescore(review_score):
    if review_score>=.99:
        return 'NEGATIVE'
    else:
        return 'NEUTRAL'

sentiment_df.loc[sentiment_df['sentiment'] == 'NEGATIVE', 'sentiment'] = sentiment_df['sentiment_score'].apply(lambda x: rescore(x))

# Sentiment date from UTC to human readable date
sentiment_df['PostDate'] = sentiment_df['PostDate'].apply(lambda x: datetime.datetime.utcfromtimestamp(x).strftime("%d %B %Y"))
# Aggregate sentiment counts by date and company
sentiment_counts = sentiment_df.groupby(['PostDate', 'CompanyRedditName'])['sentiment'].value_counts().unstack(fill_value=0)
datewise_count_df = sentiment_df.groupby(['PostDate', 'CompanyRedditName']).size().to_frame(name='count').reset_index()
datewise_count_df = datewise_count_df.sort_values(by='PostDate')
datewise_count_df = datewise_count_df[~datewise_count_df['PostDate'].str.contains("June")]
datewise_count_df = datewise_count_df.merge(sentiment_counts, on=['PostDate', 'CompanyRedditName'], how='left')
datewise_count_df['Buy/Sell'] = datewise_count_df['NEGATIVE'] - datewise_count_df['POSITIVE']


def rank_companies(df):
    # Sort by Buy/Sell (descending) and reset index (optional)
    df = df.sort_values(by='Buy/Sell', ascending=False).reset_index(drop=True)
    # Add a new 'Rank' column with integer position for each company on that date
    df['Rank'] = df.groupby('PostDate')['Buy/Sell'].transform('rank').astype(int)
    return df


# Apply the ranking function to the entire DataFrame
datewise_count_df = datewise_count_df.groupby('PostDate').apply(rank_companies).reset_index(drop=True)
print(datewise_count_df)
# Picking top and bottom 3 companies
def get_top_and_bottom_ranked(df):
  grouped_df = df.groupby('PostDate')

  # Define a function to get top and bottom ranked companies
  def get_top_bottom(group):
    # Sort by Rank (ascending for bottom 3)
    sorted_group = group.sort_values(by='Rank')
    # Top 3 companies (excluding first row for Rank 1)
    top_companies = sorted_group.iloc[:3, sorted_group.columns.get_loc('CompanyRedditName')]
    # Bottom 3 companies (excluding last row for Rank last)
    bottom_companies = sorted_group.iloc[-3:, sorted_group.columns.get_loc('CompanyRedditName')]
    return pd.Series({'Top 3 Companies': top_companies.tolist(), 'Bottom 3 Companies': bottom_companies.tolist()})

  # Apply the function to each group and reset index to include 'PostDate'
  result_df = grouped_df.apply(get_top_bottom).reset_index()
  return result_df

# Get the new DataFrame with top and bottom ranked companies
top_bottom_df = get_top_and_bottom_ranked(datewise_count_df.copy())

print(top_bottom_df)

# datewise_count_df['Top3'] =
# Now let's bring in the stock data
stock_performance_df = pd.read_csv('/Users/kirtanagopakumar/PycharmProjects/reddit_sentiment_analysis_trading_bot/stock_performance/stock_data/CompanyDataFull.csv')

# Prepare datewise_count_df for merging
top_bottom_df = top_bottom_df.rename(columns={'PostDate': 'Date_to_analyse'})

next_date = list(top_bottom_df['Date_to_analyse'])[1:]
next_date.extend(['01 June 2024'])

top_bottom_df['Date'] = next_date
print(top_bottom_df)
# Identify the company's subreddit
meta_data = pd.read_csv('/Users/kirtanagopakumar/PycharmProjects/reddit_sentiment_analysis_trading_bot/stock_performance/stock_data/CompaniesMetaData.csv')

def stock_subreddit(company):
    return meta_data.loc[meta_data['Company'] == company, 'Subreddit'].values[0]

stock_performance_df['Subreddit'] = stock_performance_df['CompanyName'].apply(lambda x: stock_subreddit(x))
def reformat_date(date_str):
    # Parse the date string
    date_obj = pd.to_datetime(date_str)
    return date_obj.strftime('%d %B %Y')


# Apply the function to the column
stock_performance_df['Date'] = stock_performance_df['Date'].apply(lambda x: reformat_date(x))
print(stock_performance_df)

# Get the closing value for top and bottom 3 companies
datewise_values_top = []
for item in range(len(top_bottom_df)):
    closing_for_date = []
    for co in top_bottom_df['Top 3 Companies'].iloc[item]:
        try:
            closing_for_date.append(stock_performance_df[(stock_performance_df['Subreddit']==co)&(stock_performance_df['Date']==top_bottom_df['Date'].iloc[item])]['Close'].iloc[0])
        except:
            # Day with no trades like the weekend
            closing_for_date.append(0)
    datewise_values_top.append(closing_for_date)

top_bottom_df['closing_values_top'] = datewise_values_top

datewise_values_bottom = []
for item in range(len(top_bottom_df)):
    closing_for_date = []
    for co in top_bottom_df['Bottom 3 Companies'].iloc[item]:
        try:
            closing_for_date.append(stock_performance_df[(stock_performance_df['Subreddit']==co)&(stock_performance_df['Date']==top_bottom_df['Date'].iloc[item])]['Close'].iloc[0])
        except:
            # Day with no trades like the weekend
            closing_for_date.append(0)
    datewise_values_bottom.append(closing_for_date)

top_bottom_df['closing_values_bottom'] = datewise_values_bottom

def sum_list(row):
  return sum(row['closing_values_top']) - sum(row['closing_values_bottom']) * 10

top_bottom_df['Net_Value'] = top_bottom_df.apply(sum_list, axis=1)

print(top_bottom_df)

amounts_made_or_lost = top_bottom_df['Net_Value'].sum()

made_or_lost = 'LOST' if amounts_made_or_lost<0 else 'MADE'
print(f'At the end of this exercise, we have {made_or_lost} {amounts_made_or_lost}')

