from distutils.log import error
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password_from_the_form = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password_from_the_form):
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('This email does not exist.', category='error')


    return render_template("login.html")

@auth.route('/logout')
def logout():
    return render_template("home.html")

@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('THis email already exists.', category='error')
        elif len(email) < 4 or '@' not in email:
            flash('Put a good email please.', category='error')
        elif len(firstname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # add user to database
            new_user = User(email=email, first_name=firstname, password=generate_password_hash(password2, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash('Account created.', category='success')
            return redirect(url_for('views.home'))
 
    return render_template("sign_up.html")
