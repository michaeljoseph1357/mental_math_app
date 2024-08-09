from flask import render_template, redirect, url_for, request, flash, current_app as app
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User
from .forms import RegistrationForm, LoginForm
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime
from app.utils.utils import generate_addition_problem


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='scrypt', salt_length=16)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Your account has been created! You are now logged in.', 'success')
        return redirect(url_for('landing'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('landing'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/landing')
@login_required
def landing():
    return render_template('landing.html')

@app.route('/module/<module_name>')
@login_required
def module_selection(module_name):
    if module_name in ['addition', 'subtraction', 'multiplication', 'division']:
        return render_template(f'modules/{module_name}_module.html', module_name=module_name)
    else:
        flash('Invalid module selected.', 'danger')
        return redirect(url_for('landing'))
    

@app.route('/addition_game/<difficulty>', methods=['GET', 'POST'])
@login_required
def start_addition_game(difficulty):
    if difficulty not in ['easy', 'medium', 'hard']:
        flash('Invalid difficulty level selected.', 'danger')
        return redirect(url_for('module_selection', module_name='addition'))
    
    if request.method == 'POST':
        # Handle the submission of an answer
        user_answer = int(request.form.get('answer'))
        correct_answer = int(request.form.get('correct_answer'))
        score = int(request.form.get('score'))
        
        if user_answer == correct_answer:
            score += 1
            flash('Correct!', 'success')
        else:
            flash('Incorrect, try the next one!', 'danger')
        
        # Generate a new problem
        num1, num2 = generate_addition_problem(difficulty)
        return render_template('games/addition_game.html', difficulty=difficulty, num1=num1, num2=num2, score=score)
    
    # Game start: Generate the first problem
    num1, num2 = generate_addition_problem(difficulty)
    return render_template('games/addition_game.html', difficulty=difficulty, num1=num1, num2=num2, score=0)

@app.route('/subtraction_game/<difficulty>')
@login_required
def start_subtraction_game(difficulty):
    if difficulty not in ['easy', 'medium', 'hard']:
        flash('Invalid difficulty level selected.', 'danger')
        return redirect(url_for('module_selection', module_name='subtraction'))
    
    # Initial game setup for subtraction can go here
    return render_template('games/subtraction_game.html', difficulty=difficulty)

@app.route('/multiplication_game/<difficulty>')
@login_required
def start_multiplication_game(difficulty):
    if difficulty not in ['easy', 'medium', 'hard']:
        flash('Invalid difficulty level selected.', 'danger')
        return redirect(url_for('module_selection', module_name='multiplication'))
    
    # Initial game setup for multiplication can go here
    return render_template('games/multiplication_game.html', difficulty=difficulty)

@app.route('/division_game/<difficulty>')
@login_required
def start_division_game(difficulty):
    if difficulty not in ['easy', 'medium', 'hard']:
        flash('Invalid difficulty level selected.', 'danger')
        return redirect(url_for('module_selection', module_name='division'))
    
    # Initial game setup for division can go here
    return render_template('games/division_game.html', difficulty=difficulty)




