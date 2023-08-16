"""Blogly application."""

from flask import Flask,request,render_template,redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db,User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "aasdfjk153825"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def root():
    """Redirects to list of users"""     
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users =User.query.all()
    return render_template('user_list.html', users = users)

@app.route('/users/new')
def show_user_form():      
    return render_template('user_form.html') 



@app.route('/users/new', methods = ["POST"])
def create_users():
    first_name = request.form["First Name"]
    last_name = request.form["Last Name"]
    image_url = request.form["Image URL"]

    new_user = User(first_name=first_name, last_name=last_name, 
                    image_url = image_url)
    db.session.add(new_user)
    db.session.commit();

    return redirect('/users')

@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user =user)

@app.route('/users/<int:user_id>/edit')
def show_user_form_edit(user_id):     
    user = User.query.get_or_404(user_id)
    return render_template("user_form_edit.html", user =user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['First Name']
    user.last_name = request.form['Last Name']
    user.image_url = request.form['Image URL']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

   

   

