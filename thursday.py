# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
import os, hashlib
import shoppinglist

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
									+"/"+str(event[2])+"/"+str(event[4]), str(event[5])))
		return render_template("calendar.html", **{"formattedEvents": formattedEvents})


@app.route('/calendar/<int:month>')
def monthly_calendar(month):
	if not session.get('logged_in'):
		return render_template("home.html")
	else:
		month = str(month)
		cur = g.db.execute("SELECT * FROM events WHERE month ="+month)
		events = cur.fetchall()
		print "Events: "
		formattedEvents = []
		for event in events:
			formattedEvents.append((str(event[1]), str(event[3])\
									+"/"+str(event[2])+"/"+str(event[4])))

		return render_template("calendar.html", **{"formattedEvents": formattedEvents})

@app.route('/calendar/add')
def add_event():
	if not session.get('logged_in_admin'):
		error = "You must be an admin to visit that page!"
		return render_template('user_homepage.html', error = error)
	else:
		return render_template("new_event.html")


@app.route('/calendar/new_event', methods = ['POST', 'GET'])
def commit_event():
	if not session.get('logged_in_admin'):
			error = "You must be an admin to visit that page!"
			return render_template('user_homepage.html', error = error)
	else:
		event_name = request.form['name']
		month, day, year = request.form['date'].split("/")
		big = 'big' in request.form

		query = "SELECT * FROM events WHERE day ='"+day+"' AND month = '"+month\
				+"' AND year = '"+year+"'"
		cur = g.db.execute(query)
		exists = cur.fetchone() != None
		if exists:
			flash("There is already an event scheduled for the\
				  date you attempted.  Please try again.")

			return redirect('/calendar')
		else:
			values = (event_name, day, month, year, big)
			values = tuple([str(x) for x in values])
			query = "INSERT INTO events (event, day, month, year, big)\
					 VALUES "+str(values)
			print query
			cur = g.db.execute(query)
			g.db.commit()
			return redirect("/calendar")

@app.route('/')
def index():
	if not session.get('logged_in'):
		return render_template("home.html")
	else:
		return render_template("user_homepage.html")




# conforms to REST (sortof)
@app.route('/shopping/list', methods=["POST", "GET"])
def shopping_list():
   
   if request.method == "POST":
	  
	  print "posting" 
	  if "id" in request.form:
		 pass # this is an update request

	  else:
		 print "posting"
		 lst = shoppinglist.ShoppingList() 
		 lst.add( request.form )
   
		 
		  
    
   s = shoppinglist.ShoppingList()  
   return render_template("shopping_list.html")
	  

@app.route('/users')
def show_users():
	if session['logged_in_admin']:
		query = "SELECT username, admin from users"
		cur = g.db.execute(query)
		userList = [x for x in cur.fetchall()]
		return render_template('users.html', **{'users': userList})
	else:
		error = "You must be an admin to visit that page!"
		return render_template('user_homepage.html', error = error)

@app.route('/users/add', methods = ['POST', 'GET'])
def add_user_form():
	if session['logged_in_admin'] == True:
			return render_template('new_user.html')
	else:
		error = "You must be an admin to visit that page!"
		return render_template('user_homepage.html', error = error)


@app.route('/users/useradd',  methods = ['POST', 'GET'])
def add_user():
	if request.method == 'POST':
		print request.form
		username = request.form["username"]
		passwd = hashlib.md5(request.form["password"]).hexdigest()
		admin = "admin" in request.form
		cur = g.db.execute("SELECT * from USERS where username = '"+username+"'")
		if cur.fetchone() != None:
			error = "User already exists"
			return render_template('new_user.html', error = error)
		else:
			query = "INSERT INTO users (username, password, admin)\
					 VALUES ('"+str(username)+"', '"+str(passwd)+"', '"+str(admin)+"')"
			print query
			g.db.execute(query)
			g.db.commit()
			return redirect("/users")
	


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		print "Trying to Auth user: " + request.form["username"]
		query = "SELECT * from users WHERE username = '"+request.form["username"]+"'"
		cur = g.db.execute(query)
		print query
		result = cur.fetchone()
		passwd = hashlib.md5(request.form["password"]).hexdigest()
		print passwd
		if result == None:
			error = 'Invalid username'
		elif passwd != result[2]:
			error = 'Invalid password for given username.'
		else:
			if result[3] == 'True':
				session['logged_in_admin'] = True
			else:
				session['logged_in_admin'] = False
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


