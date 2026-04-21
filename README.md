# 💪 Workout Tracker API

A professional RESTful API for tracking fitness routines, built with **Flask**, **SQLAlchemy**, **Flask-Migrate**, and **Marshmallow**. This API implements a many-to-many relationship between Workouts and Exercises with a dedicated join table for performance metrics.

---

## 📝 Project Description

The Workout Tracker API provides a robust backend to:

- **Manage Workouts** — Create, view, and delete sessions with date and duration tracking.
- **Manage Exercises** — Catalog exercises by category and equipment requirements.
- **Link Data** — Add exercises to specific workouts via `WorkoutExercise` records that store reps, sets, and duration.

The API enforces data integrity through a **Triple-Layer Validation** system: Database Constraints, Model Logic (`@validates`), and Marshmallow Schema Validations.

---

## 🚀 Installation

**Prerequisites:** Python 3.10+, [pipenv](https://pipenv.pypa.io/)

**1. Clone the repository

```bash
git clone <your-repo-url>
cd workout-api
```

**2. Install dependencies

```bash
pipenv install
pipenv shell
```

**3. Navigate to the server directory

```bash
cd server
```

**4. Initialize & migrate the database

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade head
```

**5. Seed the database

```bash
python seed.py
```

---

## 🏃 Running the API

From inside the `server/` directory (with `pipenv shell` active):

```bash
flask run --port 5555
```

The API will be available at `http://localhost:5555`.

---

## 📡 Endpoints

### Workouts

| Method | Endpoint | Description |
    |--------|----------|-------------|
    | `GET` | `/workouts` | List all workouts with nested exercises. |
    | `GET` | `/workouts/<id>` | Get a single workout by ID. |
    | `POST` | `/workouts` | Create a new workout session. |
    | `DELETE` | `/workouts/<id>` | Delete a workout (cascades to WorkoutExercises). |

**POST `/workouts` — request body:**

```json
{
  "date": "2024-06-10",
  "duration_minutes": 45,
  "notes": "Optional notes"
}
```

---

### Exercises

| Method | Endpoint | Description |
    |--------|----------|-------------|
| `GET` | `/exercises` | List all exercises. |
| `GET` | `/exercises/<id>` | Get a single exercise with associated workouts. |
| `POST` | `/exercises` | Create a new exercise. |
| `DELETE` | `/exercises/<id>` | Delete an exercise (cascades to WorkoutExercises). |

**POST `/exercises` — request body:**

```json
{
  "name": "Barbell Squat",
  "category": "Strength",
  "equipment_needed": true
}
```

---

### WorkoutExercises (Join Table)

| Method | Endpoint | Description |
    |--------|----------|-------------|
    | `POST` | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout. |

**POST body:**

```json
{
  "reps": 10,
  "sets": 3,
  "duration_seconds": 60
}
```

---

## 🛡️ Validations

### 1. Table Constraints (Database Level)

- `exercises.name` and `exercises.category` — Cannot be null.
- `workout_exercises.reps` and `workout_exercises.sets` — Required non-nullable fields.
- **Foreign Keys** — Enforced relationship integrity between tables.

### 2. Model Validations (`@validates`)

- `Exercise.name` — Strips whitespace and rejects strings shorter than 2 characters.
- `Workout.duration_minutes` — Must be a positive integer (> 0).

### 3. Schema Validations (Marshmallow)

- `ExerciseSchema.name` — `Length(min=2)`
- `WorkoutSchema.duration_minutes` — `Range(min=1)`
- `WorkoutExerciseSchema.reps` / `sets` — `Range(min=1)` (ensures positive input).
