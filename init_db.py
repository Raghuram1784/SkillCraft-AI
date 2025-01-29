from app import app, db
from models import User, Skill, Module
from datetime import datetime

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()

        # Add initial skills
        python_skill = Skill(
            name='Python Programming',
            description='Learn Python from basics to advanced concepts',
            category='Programming',
            difficulty_level='Beginner',
            estimated_duration='8 weeks'
        )

        # Add modules for Python skill
        modules = [
            Module(
                skill=python_skill,
                name='Python Basics',
                description='Introduction to Python programming',
                order=1,
                content='Basic syntax, variables, and data types'
            ),
            Module(
                skill=python_skill,
                name='Control Flow',
                description='Learn about control structures in Python',
                order=2,
                content='If statements, loops, and functions'
            ),
            # Add more modules as needed
        ]

        db.session.add(python_skill)
        db.session.add_all(modules)
        db.session.commit()

if __name__ == '__main__':
    init_db() 