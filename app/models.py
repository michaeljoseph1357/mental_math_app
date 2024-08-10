from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):  # Inherit from UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)



class HighScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_type = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    # Relationship to User model
    user = db.relationship('User', backref=db.backref('high_scores', lazy=True))

    def __repr__(self):
        return f'<HighScore {self.user.username} - {self.game_type} {self.difficulty}: {self.score}>'
