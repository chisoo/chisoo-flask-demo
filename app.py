from flask import Flask, render_template, request, redirect

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

		#f.open('%s.txt'%(app.vars['ticker_name']), 'w')
		#f.write('Ticker Name: %s\n'%(app.vars['ticker_name']))
		#f.close()

		return 'requested data'

if __name__ == '__main__':
	app.run(port=33507)
