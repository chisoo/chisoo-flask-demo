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

<<<<<<< HEAD
		return "Requested Data for {}".format(app.vars['ticker_name']
=======
		return "Requested Data for {}'.format(app.vars['ticker_name']"
>>>>>>> 75fd56e830cbdb3d7fc77f380517d5662e68e259

if __name__ == '__main__':
	app.run(port=33507)
