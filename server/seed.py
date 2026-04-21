from app import app
from models import *
from faker import Faker
import random

fake = Faker()

with app.app_context():
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    
    categories = ['Cardio', 'Strength', 'Flexibility', 'Balance']
    exercises = []
    for _ in range(10):
        ex = Exercise(
        name=fake.unique.word().capitalize() + " " + random.choice(['Press', 'Lift', 'Stretch', 'Run']),
        category=random.choice(categories),
        equipment_needed=random.choice([True, False])
         )
        exercises.append(ex)
        db.session.add(ex)
    
    workouts = []    
    for _ in range(5):
        wo = Workout(
        date=fake.date_this_year(),
        duration_minutes=random.randint(20, 90),
        notes=fake.sentence()
        )
        workouts.append(wo)
        db.session.add(wo)
    db.session.commit()
        
    for wo in workouts:
        selected_exercises = random.sample(exercises, random.randint(2, 4))
        for ex in selected_exercises:
            we = WorkoutExercise(
            workout_id=wo.id,
            exercise_id=ex.id,
            reps=random.randint(5, 15),
            sets=random.randint(1, 5),
            duration_seconds=random.randint(30, 300)
            )
            db.session.add(we)
        
    db.session.commit()