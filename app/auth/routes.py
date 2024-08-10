from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..forms import RegistrationForm, LoginForm
from ..models import User, HighScore
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/dashboard')
@login_required
def dashboard():
    # Fetch user information
    user = current_user

    # Fetch high scores for the current user
    high_scores = HighScore.query.filter_by(user_id=user.id).all()

    # Organize the high scores by game type and difficulty
    scores_by_game = {
        'addition': {'easy': None, 'medium': None, 'hard': None},
        'subtraction': {'easy': None, 'medium': None, 'hard': None},
        'multiplication': {'easy': None, 'medium': None, 'hard': None},
        'division': {'easy': None, 'medium': None, 'hard': None},
    }

    for score in high_scores:
        if score.game_type in scores_by_game:
            scores_by_game[score.game_type][score.difficulty] = score.score

    return render_template('dashboard.html', user=user, scores_by_game=scores_by_game)


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