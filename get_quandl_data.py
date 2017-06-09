import quandl
import os
from datetime import timedelta

quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')
ticker_name = 'AAPL'
quandl_tag = 'WIKI/' + ticker_name
quandl_data = quandl.get(quandl_tag)

# keep only necessary columns
quandl_data = quandl_data[['Close', 'Adj. Close', 'Open', 'Adj. Open']]
quandl_data.reset_index(inplace = True)

# keep only the last month data
start_date = quandl_data['Date'].max() - timedelta(days = 30)
quandl_data = quandl_data[quandl_data['Date'] >= start_date]
quandl_data.reset_index(drop = True, inplace = True)

print(quandl_data)