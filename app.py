from flask import Flask, render_template, request, redirect
import quandl
import os
from datetime import timedelta

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
		print('test')

		return "Requested Data"

if __name__ == '__main__':
	app.run(port=33507)
