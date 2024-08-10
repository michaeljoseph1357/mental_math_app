from flask import render_template, redirect, url_for, request, flash, current_app as app
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User
from .forms import RegistrationForm, LoginForm
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime
from app.utils.utils import generate_problem, update_high_score
from app.models import HighScore, db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/landing')
@login_required
def landing():
    return render_template('landing.html')

