# Repository - Reddit Sentiment Analysis Trading Bot

### This repository contains code analysing a set of 10 companies belonging to the S&P 100. A trading bot was built to track profits/losses over a period of one month. Trades are executed by the code based on net aggregate sentiment gleaned from Reddit posts/comments during this period

<img src="https://images.unsplash.com/photo-1640340434855-6084b1f4901c?q=80&w=2000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="alt text" width="300"/>

### Objective- 
To determine whether there is a correlation between social media sentiment and stock performance

### INTRODUCTION-
#### Companies selected-
| Serial No. | Company Name | Ticker | Industry | Stock Exchange |
|---|---|---|---|---|
| 1 | Microsoft Corp | MSFT | Information Technology | NASDAQ |
| 2 | Apple Inc. | AAPL | Information Technology | NASDAQ |
| 3 | Nvidia Corp | NVDA | Information Technology | NASDAQ |
| 4 | Amazon.com Inc | AMZN | Consumer Discretionary | NASDAQ |
| 5 | Alphabet Inc A | GOOGL | Communication Services | NASDAQ |
| 6 | Meta Platforms, Inc. Class A | META | Communication Services | NASDAQ |
| 7 | Tesla | TSLA | Consumer Discretionary | NASDAQ |
| 8 | Walmart | WMT | Consumer Defensive | NYSE |
| 9 | Netflix | NFLX | Communication Services | NASDAQ |
| 10 | Walt Disney | DIS | Consumer Discretionary | NYSE |


#### Data collected- 
1. Reddit - Reddit posts from the past 1 month were collected based using the PRAW package and Reddit API.
2. Stock performance - Yahoo Finance's yfinance package was used to collect the stock performance for the past 1 month


#### Data sentiment- 
Transformers were used to then compute general sentiment of the collected reddit posts.


#### Data normalisation-
Reddit being a generally negative platform, it was unsurprising that the sentiment computed was largely negative. Thus, the sentiment score was used to normalise the negative value and put them on an analysable 'scale'.
