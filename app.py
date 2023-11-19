"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'blogly-secret-key'
debug = DebugToolbarExtension(app)


@app.before_first_request
def create_tables():
    """Create all tables."""
    db.create_all()

@app.route('/')
def home():
    """Redirect to list of users."""

    return redirect('/users')

@app.route('/users')
def list_users():
    """Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form.
    """
    users = User.query.all()
    return render_template("list.html", users=users)

@app.route('/users/new')
def add_user():
    """Show an add form for users."""

    return render_template('user_form.html')

@app.route('/users/new', methods=["POST"])
def user_added():
    """Process the add form, adding a new user and going back to /users."""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/user/<int:user_id>')
def user_details(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route("/user/<int:user_id>/edit")
def edit_page(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user_id=user_id)

@app.route("/user/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Process the edit form, returning the user to the /users page."""
    edited_user = User.query.get_or_404(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    edited_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(edited_user)
    db.session.commit()
    return redirect('/users')

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Delete the user."""

    deleted_user = User.query.get_or_404(user_id)

    delete_user = User.query.filter_by(user_id = user_id).delete()
    
    db.session.commit()
    return redirect('/users')



if __name__ == '__main__':
    app.run(debug=True)