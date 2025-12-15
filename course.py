from flask import Blueprint, request, jsonify, make_response
from db import get_connection
from auth import token_required

courses_bp = Blueprint('course', __name__)

# CREATE
@courses_bp.route("/course", methods=["POST"])
@token_required
def create_course():
    data = request.json
    required = ["course_name", "Teacher_idTeacher"]
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO course (course_name, Teacher_idTeacher) VALUES (%s, %s)",
        (data["course_name"], data["Teacher_idTeacher"])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Course created"}), 201

# READ ALL
@courses_bp.route("/courses", methods=["GET"])
def get_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM course")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "course_name": r[1], "Teacher_idTeacher": r[2]} for r in rows]), 200

# UPDATE
@courses_bp.route("/course/<int:id>", methods=["PUT"])
@token_required
def update_course(id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE course SET course_name=%s, Teacher_idTeacher=%s WHERE idCourse=%s",
        (data["course_name"], data["Teacher_idTeacher"], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Course updated"}), 200

# DELETE
@courses_bp.route("/course/<int:id>", methods=["DELETE"])
@token_required
def delete_course(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM course WHERE idCourse=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Course deleted"}), 200

# SEARCH
@courses_bp.route("/course/search", methods=["GET"])
def search_course():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Name query required"}), 400
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM course WHERE course_name LIKE %s", (f"%{name}%",))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "course_name": r[1], "Teacher_idTeacher": r[2]} for r in rows]), 200
