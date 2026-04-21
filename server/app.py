from flask import Flask, make_response, request
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise
from schemas import *

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'GET':
        workouts = Workout.query.all()
        return make_response(workouts_schema.dump(workouts), 200)
    
    if request.method == 'POST':
        json_data = request.get_json()
        try:
            # Schema Validation
            data = workout_schema.load(json_data)
            new_workout = Workout(**data)
            db.session.add(new_workout)
            db.session.commit()
            return make_response(workout_schema.dump(new_workout), 201)
        except Exception as e:
            return make_response({"errors": str(e)}, 400)

@app.route('/workouts/<int:id>', methods=['GET', 'DELETE'])
def workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    if request.method == 'GET':
        return make_response(workout_schema.dump(workout), 200)
    
    if request.method == 'DELETE':
        db.session.delete(workout)
        db.session.commit()
        return make_response({}, 204)

@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == 'GET':
        exercises = Exercise.query.all()
        return make_response(exercises_schema.dump(exercises), 200)
    
    if request.method == 'POST':
        json_data = request.get_json()
        try:
            data = exercise_schema.load(json_data)
            new_exercise = Exercise(**data)
            db.session.add(new_exercise)
            db.session.commit()
            return make_response(exercise_schema.dump(new_exercise), 201)
        except Exception as e:
            return make_response({"errors": str(e)}, 400)

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    json_data = request.get_json()
    if not Workout.query.get(workout_id) or not Exercise.query.get(exercise_id):
        return make_response({"error": "Workout or Exercise not found"}, 404)
    
    try:
        json_data['workout_id'] = workout_id
        json_data['exercise_id'] = exercise_id
        data = workout_exercise_schema.load(json_data)
        
        new_we = WorkoutExercise(**data)
        db.session.add(new_we)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(new_we), 201)
    except Exception as e:
        return make_response({"errors": str(e)}, 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)