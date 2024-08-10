from flask import render_template
from flask_login import current_user
from . import progress
from ..models import HighScore  # Import your HighScore model

@progress.route('/<game_type>')
def progress(game_type):
    # Query the database to get the high scores for the current user, game_type, and difficulty levels
    high_scores = {
        'easy': HighScore.query.filter_by(user_id=current_user.id, game_type=game_type, difficulty='easy').order_by(HighScore.score.desc()).first(),
        'medium': HighScore.query.filter_by(user_id=current_user.id, game_type=game_type, difficulty='medium').order_by(HighScore.score.desc()).first(),
        'hard': HighScore.query.filter_by(user_id=current_user.id, game_type=game_type, difficulty='hard').order_by(HighScore.score.desc()).first(),
    }

    # Extract scores or set default if no score exists
    high_scores = {
        'easy': high_scores['easy'].score if high_scores['easy'] else 0,
        'medium': high_scores['medium'].score if high_scores['medium'] else 0,
        'hard': high_scores['hard'].score if high_scores['hard'] else 0,
    }

    return render_template('progress.html', game_type=game_type, high_scores=high_scores)
