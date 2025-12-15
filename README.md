# Student Management API

A Flask-based REST API for managing students, courses, and authentication. It supports JWT authentication, MySQL persistence, and standard CRUD operations.

## Features
- JWT authentication for protected endpoints
- CRUD operations for students and courses
- MySQL database persistence
- Search and filtering capabilities

## Requirements
- Python 3.14
- MySQL Server
- Packages in [requirements.txt](requirements.txt)

## Installation
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration
The app reads configuration from environment variables (with sane defaults):
- `MYSQL_HOST` (default: `localhost`)
- `MYSQL_USER` (default: `root`)
- `MYSQL_PASSWORD` (default: `Root`)
- `MYSQL_DB` (default: `mydb`)
- `SECRET_KEY` (default: `CSelect1`)

## Running

Python
```command prompt
python app.py
```

## API Usage
Base URL: http://localhost:5000

### Authentication
**POST /auth/login** — body:
```json
{
  "username": "admin",
  "password": "admin123"
}
```
Response:
```json
{
  "token": "<jwt_token>",
  "expires_at": "2025-12-15T12:00:00"
}
```
Use the token in headers for protected routes:
```
Authorization: Bearer <jwt_token>
```

### Students
- **GET /students** — list all students
- **GET /students/<id>** — get a specific student
- **POST /students** (auth) — add a student:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "age": 20,
  "gender": "male",
  "course_id": 1
}
```
- **PUT /students/<id>** (auth) — update a student (partial updates allowed)
- **DELETE /students/<id>** (auth) — remove a student

### Courses
- **GET /courses** — list all courses
- **GET /courses/<id>** — get a specific course
- **POST /courses** (auth) — add a course:
```json
{
  "name": "Computer Science"
}
```
- **PUT /courses/<id>** (auth) — update a course
- **DELETE /courses/<id>** (auth) — remove a course

## Examples
Get all students:
```bash
curl http://localhost:5000/students
```
Add a student (with auth token):
```bash
curl -X POST http://localhost:5000/students \
-H "Authorization: Bearer <jwt_token>" \
-H "Content-Type: application/json" \
-d '{"first_name":"John","last_name":"Doe","age":20,"gender":"male","course_id":1}'
```

## Notes
- Ensure foreign key constraints are respected: student course_id must exist in courses.
- All SQL queries are parameterized to prevent SQL injection.
- JWT tokens expire according to JWT_EXPIRATION_DELTA.

## Project Structure
- `app.py` — main entrypoint for Flask
- `students.py` — student routes and logic
- `courses.py` — course routes and logic
- `teachers.py` — teachers routes and logic
- `auth.py` — authentication routes and JWT logic
- `db.py` — database connection utility
- `requirements.txt` — dependencies
- `README.md` — this documentation

