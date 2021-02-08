import requests
import pandas as pd


# get fundamental data for 
def get_fin_data(tickerlist, report_type):
    df = pd.DataFrame()
    for ticker in tickerlist:
      try: 
        url = 'https://api.polygon.io/v2/reference/financials/' + ticker + '?type=' + report_type + '&apiKey=AKD9NA6TPAY71JOD3TQJ'
                
        # gets results in dataframe
        data = requests.get(url).json()
        df1 = pd.DataFrame(data['results'])

        # shares column has # of outstanding shares
        df = df.append(df1)
        print(ticker + " (" + str(tickerlist.index(ticker) + 1) + "/" + str(len(tickerlist)) + "): SUCCESS")
      except:
        print(ticker + " (" + str(tickerlist.index(ticker) + 1) + "/" + str(len(tickerlist)) + "): FAILURE")
    return df
    

# returns unadjusted quarterly fin data
tickerlist = ['AAPL', 'GOOGL']

# report_type: Q = quarterly, A = Annual, QA = quarterly annualized
df = get_fin_data(tickerlist, 'Q')

# stores data in csv

df.to_csv('fundamental-data.csv')
df
