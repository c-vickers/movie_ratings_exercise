"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
	"""Show list of users."""

	users = User.query.all()
	return render_template("user_list.html", users=users)

@app.route("/login")
def login():
	"""User login form"""

	return render_template("login.html")

@app.route("/process_login", methods=["POST"])
def process_login():
	"""Return users to homepage after verifying login info"""
	
	username = request.form.get("username")
	password = request.form.get("password")
	#use .first() instead of all 
	check_user = User.query.filter_by(email = username).first() 
	if check_user == None:
		return render_template("new_user.html") #If None route to new user sign up page...
	#...create an html form that posts to database and reroutes to homepage
	else: # If username in User
		if password == check_user.password:
			session['user_id'] = check_user.user_id
			flash('You are now logged in!') # Add a flash message to tell them they are logged in
			return render_template("homepage.html")
		#verify password entered matches password in User for username
		else:
			flash('Your password and username didn\'t match')

	return render_template("login.html")


@app.route("/add_user", methods=['POST'])
def add_user():
	username = request.form.get("username")
	password = request.form.get("authen")
	age = request.form.get("age")
	zipcode = request.form.get("zip")

	new_user = User(email=username, password=password, age=age, zipcode=zipcode)

	db.session.add(new_user)
	db.session.commit()

	flash('You are now registered!')

	return render_template('homepage.html')


@app.route("/logout")
def logout():
	session['user_id'] = None
	flash("You are now logged out.")

	return render_template('homepage.html')

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
