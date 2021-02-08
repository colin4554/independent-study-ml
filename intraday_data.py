import pandas_market_calendars as mcal
import requests
import pandas as pd
from datetime import datetime, timedelta


# from polygon.io
API_KEY = 


def get_stock_data(tickerlist, type, startDate, toDate, isUnadjusted, limit):
  if type == 'intraday':
    df1 = pd.DataFrame()
    startTime = datetime.strptime(datetime.now().strftime('%H:%M:%S'), '%H:%M:%S')
    for ticker in tickerlist:
    
      # gets days the exchange is open and allows us to call the function for each daya
      trading_days = mcal.get_calendar('NASDAQ').schedule(start_date=startDate, end_date=toDate)['market_open'].dt.date

      fromDate = trading_days[0]
      toDate = trading_days[-1]
      
      count = 0
      while fromDate != toDate or count == limit :
        
        # change url to be more specific (adjusted, limit, etc.)
        # url = 'https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/minute/2020-10-14/2020-10-14?unadjusted=false&sort=asc&limit=40000&apiKey=*'
        url = 'https://api.polygon.io/v2/aggs/ticker/' + ticker + '/range/1/minute/' + str(fromDate) + '/' + str(toDate) + '?unadjusted=' +str(isUnadjusted) + '&sort=asc&limit=' + str(limit) + '&apiKey=' + API_KEY
        
        # gets results in dataframe
        data = requests.get(url).json()
        df = pd.DataFrame(data['results'])
        count = len(df)
        print(ticker + " (" + str(tickerlist.index(ticker) + 1) + "/" + str(len(tickerlist)) + "): " + str(startDate) + " to " + str(fromDate))
        
        # changes unix ms to datetime
        df['hex'] = df['t']
        df['t'] = pd.to_datetime(df['t'], unit='ms')
        df['t'] = df['t'] - timedelta(hours=5, minutes=00)

        # splits time into date and time
        df['d'] = df['t'].dt.date
        df['t'] = df['t'].dt.time
        fromDate = df['d'].iloc[-1]

        # adds ticker column to seperate
        df['ticker'] = ticker
        df1 = df1.append(df)

    # final touches for dataframe
    df1 = df1.drop_duplicates()
    df1 = df1.rename(columns={'d': 'date','t': 'time', 'o': 'open', 'c': 'close', 'l': 'low', 'h': 'high', 'v': 'volume'})
    df1 = df1.drop(columns=['vw', 'n', 'hex'])
    df1 = df1.reset_index(drop=True)
    print(str(datetime.strptime(datetime.now().strftime('%H:%M:%S'), '%H:%M:%S') - startTime) + " elapsed")
    return df1
  else:
    print("Type: \'" + type + "\' not currently supported")

# calls function
tickerlist = ['AAPL', 'AMZN', 'GOOG', 'FB', 'MSFT', 'CRM']
df = get_stock_data(tickerlist, 'intraday', startDate='2018-5-20', toDate='2018-6-23', isUnadjusted = False, limit = 40000)

# stores data in csv
df.to_csv('intraday_data.csv')
df
