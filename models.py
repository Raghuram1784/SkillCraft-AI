from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    current_streak = db.Column(db.Integer, default=0)
    streak_freezes = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime)
    is_premium = db.Column(db.Boolean, default=False)
    
    # Relationships
    skills = db.relationship('UserSkill', back_populates='user')
    progress = db.relationship('Progress', back_populates='user')
    reminders = db.relationship('Reminder', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    difficulty_level = db.Column(db.String(20))
    estimated_duration = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    users = db.relationship('UserSkill', back_populates='skill')
    modules = db.relationship('Module', back_populates='skill')

class UserSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, paused
    
    # Relationships
    user = db.relationship('User', back_populates='skills')
    skill = db.relationship('Skill', back_populates='users')

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer)
    content = db.Column(db.Text)
    
    # Relationships
    skill = db.relationship('Skill', back_populates='modules')
    progress = db.relationship('Progress', back_populates='module')

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    completion_status = db.Column(db.Float, default=0.0)  # Percentage completed
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='progress')
    module = db.relationship('Module', back_populates='progress')

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    reminder_date = db.Column(db.DateTime, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    
    # Relationships
    user = db.relationship('User', back_populates='reminders') 