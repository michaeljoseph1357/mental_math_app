from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..forms import RegistrationForm, LoginForm, UpdateProfileForm, UpdatePasswordForm
from ..models import User, HighScore
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/profile')
@login_required
def profile():
    profile_form = UpdateProfileForm(obj=current_user)
    password_form = UpdatePasswordForm()
    
    if profile_form.validate_on_submit():
        current_user.username = profile_form.username.data
        db.session.commit()
        flash('Your username has been updated!', 'success')
        return redirect(url_for('auth.profile'))

    if password_form.validate_on_submit():
        # Handle password change logic here
        current_user.set_password(password_form.password.data)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('profile.html', profile_form=profile_form, password_form=password_form)

@auth.route('/landing')
@login_required
def landing():
    return render_template('landing.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='scrypt', salt_length=16)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Your account has been created! You are now logged in.', 'success')
        return redirect(url_for('auth.landing'))
    
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('auth.landing'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))