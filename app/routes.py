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

@app.route('/module_selection/<game_type>')
@login_required
def module_selection(game_type):
    valid_game_types = ['addition', 'subtraction', 'multiplication', 'division']
    
    if game_type not in valid_game_types:
        flash('Invalid game type selected.', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('modules/module_selection.html', game_type=game_type)
    

@app.route('/<game_type>_game/<difficulty>', methods=['GET', 'POST'])
@login_required
def start_game(game_type, difficulty):
    if difficulty not in ['easy', 'medium', 'hard']:
        flash('Invalid difficulty level selected.', 'danger')
        return redirect(url_for('module_selection', game_type=game_type))

    operation_map = {
        'addition': {'symbol': '+', 'operation': lambda x, y: x + y},
        'subtraction': {'symbol': '-', 'operation': lambda x, y: x - y},
        'multiplication': {'symbol': '*', 'operation': lambda x, y: x * y},
        'division': {'symbol': '/', 'operation': lambda x, y: x // y if y != 0 else 0}  # Integer division, avoid division by zero
    }

    if game_type not in operation_map:
        flash('Invalid game type selected.', 'danger')
        return redirect(url_for('dashboard'))

    operation_symbol = operation_map[game_type]['symbol']
    operation_func = operation_map[game_type]['operation']

    timer_value = app.config['TIMER_VALUE']

    if request.method == 'POST':
        # Get the user's answer, handle empty input by setting it to None or a default value
        user_answer = request.form.get('answer')
        if user_answer is None or user_answer == '':
            user_answer = None
        else:
            user_answer = int(user_answer)
        correct_answer = int(request.form.get('correct_answer'))
        score = int(request.form.get('score'))
        time_left = int(request.form.get('time_left'))

        if user_answer == correct_answer:
            score += 1
            flash('Correct!', 'success')
        else:
            flash('Incorrect, try the next one!', 'danger')
        
        # Generate a new problem
        num1, num2 = generate_problem(difficulty, game_type)
        correct_answer = operation_func(num1, num2)

        return render_template('games/game_base.html', difficulty=difficulty, game_type=game_type, operation_symbol=operation_symbol, num1=num1, num2=num2, score=score, time_left=time_left, timer_value=timer_value, correct_answer=correct_answer)

    # Initial game start
    num1, num2 = generate_problem(difficulty, game_type)
    correct_answer = operation_func(num1, num2)

    return render_template('games/game_base.html', difficulty=difficulty, game_type=game_type, operation_symbol=operation_symbol, num1=num1, num2=num2, score=0, time_left=timer_value, timer_value=timer_value, correct_answer=correct_answer)


@app.route('/game_over', methods=['POST'])
@login_required
def game_over():
    try:
        game_type = request.form.get('game_type')
        difficulty = request.form.get('difficulty')
        score = int(request.form.get('score'))
        
        # Validate game_type and difficulty
        if game_type not in ['addition', 'subtraction', 'multiplication', 'division']:
            flash('Invalid game type.', 'danger')
            return redirect(url_for('landing'))
        if difficulty not in ['easy', 'medium', 'hard']:
            flash('Invalid difficulty level.', 'danger')
            return redirect(url_for('landing'))

        # Update high score and fetch updated high score
        new_high_score = update_high_score(current_user, game_type, difficulty, score)
        high_score = HighScore.query.filter_by(user_id=current_user.id, game_type=game_type, difficulty=difficulty).first()

        return render_template('game_over.html', score=score, high_score=high_score.score, is_new_high_score=(high_score.score == new_high_score), game_type=game_type, difficulty=difficulty)

    except Exception as e:
        print(f"Error occurred: {e}")
        flash('An error occurred while processing your request.', 'danger')
        return redirect(url_for('landing'))

