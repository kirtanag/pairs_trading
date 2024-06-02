# Import packages
import os
import praw
from dotenv import load_dotenv
import datetime
from dataclasses import dataclass
import pandas as pd


# Define the dataclass
@dataclass
class RedditPostData:
    CompanyRedditName : str
    PostTitle : str
    PostBody : str
    PostDate : datetime


# Load credentials
load_dotenv()
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')


# Set up companies needed in a list
companies_analysed = ['Microsoft', 'Apple', 'Nvidia', 'Amazon', 'Google', 'Facebook', 'teslamotors', 'Walmart', 'Netflix', 'Disney']


# Initialize the PRAW instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='Test app')

# Defining time
current_time = datetime.datetime.utcnow()
one_month_ago = current_time - datetime.timedelta(days=32)

# Convert datetime to UNIX timestamp
one_month_ago_timestamp = int(one_month_ago.timestamp())
current_timestamp = int(current_time.timestamp())


# Define the search query and timeframe
reddit_post_data = []
for subreddit in companies_analysed:
    # get top posts from the company subreddit
    submissions = reddit.subreddit(subreddit).new(limit=2000)
    post_details = []
    for post in submissions:
        if post.created_utc>=one_month_ago_timestamp:
            post_data = RedditPostData(CompanyRedditName=subreddit,
                                        PostTitle = post.title,
                                        PostBody = post.selftext,
                                        PostDate = post.created_utc)
            post_details.append(post_data)
    print(f'Posts for subreddit {subreddit}: {len(post_details)}')
    for post_item in post_details:
        reddit_post_data.append(post_item)

print(len(reddit_post_data))

# Convert to CSV
pd.DataFrame(reddit_post_data).to_csv('/Users/kirtanagopakumar/PycharmProjects/reddit_sentiment_analysis_trading_bot/reddit_scraper/reddit_data/CompanySubredditDataFull.csv')
