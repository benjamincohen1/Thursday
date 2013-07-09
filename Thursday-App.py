# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
import os
# configuration
DATABASE = os.getcwd()+'/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

# DID ALL OF THE BELOW WITHOUT AN INTERNET CONNECTION
# SO I DIDN'T HAVE ACCSES TO DOCUMENTATION FOR DATETIME
# ALSO I WANTED TO HASHTAG THIS BUT IT JUST LOOKS LIKE A COMMENT
# #YOLO #PYTHONPROBLEMS 


@app.route('/calendar')
def calendar():

	if not session.get('logged_in'):
		return render_template("home.html")
	else:
		cur = g.db.execute("SELECT * FROM events")
		events = cur.fetchall()
		print "Events: "
		formattedEvents = []
		for event in events:
			formattedEvents.append((str(event[1]), str(event[3])\
									+"/"+str(event[2])+"/"+str(event[4])))

		return render_template("calendar.html", **{"formattedEvents": formattedEvents})


@app.route('/calendar/<int:month>')
def monthly_calendar(month):
	if not session.get('logged_in'):
		return render_template("home.html")
	else:
		month = str(month)
		cur = g.db.execute("SELECT * FROM events WHERE month ="+month,
						   {'mon': month})
		events = cur.fetchall()
		print "Events: "
		formattedEvents = []
		for event in events:
			formattedEvents.append((str(event[1]), str(event[3])\
									+"/"+str(event[2])+"/"+str(event[4])))

		return render_template("calendar.html", **{"formattedEvents": formattedEvents})


@app.route('/')
def index():
	if not session.get('logged_in'):
		return render_template("home.html")
	else:
		return render_template("user_homepage.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			#flash('You were logged in')
			return render_template('user_homepage.html')
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return render_template('home.html')

if __name__ == '__main__':
	connect_db()
	app.run()


