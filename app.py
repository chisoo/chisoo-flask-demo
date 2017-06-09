from flask import Flask, render_template, request, redirect

import requests
import quandl
import os
from datetime import timedelta
import pandas as pd

# from bokeh.palettes import Spectral11
# from bokeh.plotting import figure
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
		ticker_name = 'AAPL'
		quandl_tag = 'WIKI/' + ticker_name
		quandl_df = quandl.get(quandl_tag)

		# keep only necessary columns
		quandl_df = quandl_df[['Close', 'Adj. Close', 'Open', 'Adj. Open']]
		quandl_df.reset_index(inplace = True)

		# keep only the last month data
		start_date = quandl_df['Date'].max() - timedelta(days = 30)
		quandl_df = quandl_df[quandl_df['Date'] >= start_date]
		quandl_df.reset_index(drop = True, inplace = True)

		# num_lines = len(quandl_df.columns)
		# mypalette = Spectral11[0: num_lines]

		# plot = figure(title = 'Data from Quandl WIKI set', 
		# 	x_axis_label = 'date', 
		# 	x_axis_type = 'datetime')
		# plot.multi_line(xs = [quandl_df.index.values] * num_lines, 
		# 	ys = [quandl_df[col].values for col in quandl_df], 
		# 	line_color = mypalette, line_width = 5)
		data = dict(CLOSE = quandl_df['Close'], Date = quandl_df['Date'])
		plot = TimeSeries(data, \
			title = 'plot title placeholder', ylabel = 'Stock Prices')

		script, div = components(plot)

		return render_template('graph.html', script = script, div = div, ticker_name = app.vars['ticker_name'])

		# return 'testing'

if __name__ == '__main__':
	app.run(port=33507)
