from flask import Flask, render_template, request, redirect
import quandl
import os
from datetime import timedelta

from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

app.vars = {}

# create the main plot
def create_plot():
	plot = figure()
	plot.circle([1, 2], [3, 4])

	return plot

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
		quandl_data = quandl.get(quandl_tag)

		# keep only necessary columns
		quandl_data = quandl_data[['Close', 'Adj. Close', 'Open', 'Adj. Open']]
		quandl_data.reset_index(inplace = True)

		# keep only the last month data
		start_date = quandl_data['Date'].max() - timedelta(days = 30)
		quandl_data = quandl_data[quandl_data['Date'] >= start_date]
		quandl_data.reset_index(drop = True, inplace = True)

		plot = create_plot()
		script, div = components(plot)

		return render_template('index1.html', script = script, div = div)

if __name__ == '__main__':
	app.run(port=33507)
