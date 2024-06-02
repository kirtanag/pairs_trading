# # Import packages
# import os
# import praw
# from dotenv import load_dotenv
# import datetime
# from dataclasses import dataclass
#
#
# # Define the dataclass
# @dataclass
# class RedditPostData:
#     CompanyRedditName : str
#     PostTitle : str
#     PostBody : str
#     PostDate : datetime
#
#
# # Load credentials
# load_dotenv()
# client_id = os.environ.get('CLIENT_ID')
# client_secret = os.environ.get('CLIENT_SECRET')
#
#
# # Set up companies needed in a list
# stock_subreddits = ['stocks', 'StocksAndTrading']
# companies_analysed = ['Microsoft', 'Apple', 'Nvidia', 'Amazon', 'Google', 'Facebook', 'Tesla', 'Walmart', 'Netflix', 'Disney']
#
#
# # Initialize the PRAW instance
# reddit = praw.Reddit(client_id=client_id,
#                      client_secret=client_secret,
#                      user_agent='Test app')
#
# # Defining time
# current_time = datetime.datetime.utcnow()
# one_month_ago = current_time - datetime.timedelta(days=32)
#
# # Convert datetime to UNIX timestamp
# one_month_ago_timestamp = int(one_month_ago.timestamp())
# current_timestamp = int(current_time.timestamp())
#
#
# # Define the search query and timeframe
# reddit_post_data = []
# for subreddit in stock_subreddits:
#         for co in companies_analysed:
#             query = co
#             # Search for submissions
#             submissions = reddit.subreddit(subreddit).search(query, sort='new', time_filter='all', limit=2000)
#
#             # Filter submissions within the last one month, get relevant post details
#             filtered_submissions = [submission.title for submission in submissions if one_month_ago_timestamp <= submission.created_utc]
#             # print(len(filtered_submissions))
#             posts_data = []
#             for filtered_submission in filtered_submissions:
#                 post_data = RedditPostData(CompanyRedditName = subreddit,
#                                                 PostTitle = filtered_submission.title,
#                                                 PostBody = filtered_submission.body,
#                                                 PostDate = filtered_submission.created_utc)
#                 posts_data.append(post_data)
#
#     for post_item in reddit_post_data:
#         reddit_post_data.append(post_item)
#
