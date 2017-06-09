from flask import Flask, render_template, request, redirect

import requests
import quandl
import os
from datetime import timedelta
import pandas as pd

from bokeh.charts import TimeSeries, output_file
from bokeh.embed import components

app = Flask(__name__)

app.vars = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else: 
		app.vars['ticker_name'] = request.form['ticker']

		# download the data for the ticker
		quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')
		ticker_name = app.vars['ticker_name']
		quandl_tag = 'WIKI/' + ticker_name
		quandl_df = quandl.get(quandl_tag)

		# keep only necessary columns
		quandl_df = quandl_df[['Close', 'Adj. Close', 'Open', 'Adj. Open']]
		quandl_df.reset_index(inplace = True)

		# keep only the last month data
		start_date = quandl_df['Date'].max() - timedelta(days = 30)
		quandl_df = quandl_df[quandl_df['Date'] >= start_date]
		quandl_df.reset_index(drop = True, inplace = True)

		# set up tuples for dictionary
		close_tuple = ('Close', quandl_df['Close'])
		adj_close_tuple = ('Adj. Close', quandl_df['Adj. Close'])
		open_tuple = ('Open', quandl_df['Open'])
		adj_open_tuple = ('Adj. Open', quandl_df['Adj. Open'])

		list_for_plot = [('Date', quandl_df['Date'])]
		list_for_plot.append(close_tuple)
		list_for_plot.append(adj_close_tuple)
		list_for_plot.append(open_tuple)
		list_for_plot.append(adj_open_tuple)

		data = dict(list_for_plot)

		plot = TimeSeries(data, x = 'Date', \
			ylabel = 'Stock Prices')

		script, div = components(plot)

		return render_template('graph.html', script = script, div = div, ticker_name = app.vars['ticker_name'])

if __name__ == '__main__':
	app.run(port=33507)
