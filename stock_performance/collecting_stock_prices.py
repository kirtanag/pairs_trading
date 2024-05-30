# Import packages
import yfinance as yf
from dataclasses import dataclass
import datetime
import pandas as pd


# Collect the metadata of all 10 companies and arrange them in a dataclass
@dataclass
class MetaData:
    ID : str
    CompanyName : str
    Ticker : str
    Industry : str
    StockExchange : str
    Date : datetime
    Open : float
    High : float
    Low : float
    Close : float
    AdjClose : float
    Volume : float


# Define the ticker symbols and desired time period
df_tickers = pd.read_excel('/Users/kirtanagopakumar/PycharmProjects/reddit_sentiment_analysis_trading_bot/CompaniesMetaData.xlsx')
tickers = list(df_tickers['Tickers'])
period = "1mo"  # Past 1 month

# Download historical data
data_collected = []
for ticker in tickers:
    data = yf.download(ticker, period=period)
    data_collected.append(data)

print(data_collected)


