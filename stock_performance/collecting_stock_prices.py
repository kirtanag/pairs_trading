# Import packages
import yfinance as yf
from dataclasses import dataclass
import datetime
import pandas as pd


# Define the dataclass
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
df_tickers = pd.read_csv('/stock_performance/stock_data/CompaniesMetaData.csv')
tickers = list(df_tickers['Ticker'])
period = "3mo"  # Past 3 month

# Download historical data
data_collected = []
company_data = []
for ticker in tickers:
    data = yf.download(ticker, period=period)
    company_name = df_tickers[df_tickers['Ticker'] == ticker]["Company"].tolist()[0]
    industry = df_tickers[df_tickers['Ticker'] == ticker]["Industry"].tolist()[0]
    stock_exchange = df_tickers[df_tickers['Ticker'] == ticker]["Stock Exchange"].tolist()[0]

    # Iterate through each day in the downloaded data
    for index, row in data.iterrows():
        # Create a MetaData object for each day's data
        meta_data = MetaData(
            ID=ticker + str(index.date()),
            CompanyName=company_name,
            Ticker=ticker,
            Industry=industry,
            StockExchange=stock_exchange,
            Date=index.date(),
            Open=row["Open"],
            High=row["High"],
            Low=row["Low"],
            Close=row["Close"],
            AdjClose=row["Adj Close"],
            Volume=row["Volume"],
        )

        # Append the object to the list
        company_data.append(meta_data)


# Convert to CSV
pd.DataFrame(company_data).to_csv('/stock_performance/stock_data/CompanyDataFull.csv')


