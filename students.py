from flask import Blueprint, request, jsonify, make_response
from db import get_connection
from auth import token_required
import xml.etree.ElementTree as ET

students_bp = Blueprint('student', __name__)


# CREATE

@students_bp.route("/student", methods=["POST"])
@token_required
def create_student():
    data = request.json

    required = ["first_name", "last_name", "age", "gender", "course_id"]
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO student (first_name, last_name, age, gender, Course_idCourse)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            data["first_name"],
            data["last_name"],
            data["age"],
            data["gender"],
            data["course_id"]
        )
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Student created"}), 201

@students_bp.route("/students", methods=["GET"])
def get_students():
    format = request.args.get("format", "json")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if format.lower() == "xml":
        root = ET.Element("students")
        for r in rows:
            s = ET.SubElement(root, "student")
            ET.SubElement(s, "id").text = str(r[0])
            ET.SubElement(s, "first_name").text = r[1]
            ET.SubElement(s, "last_name").text = r[2]
            ET.SubElement(s, "age").text = str(r[3])
            ET.SubElement(s, "gender").text = r[4]
            ET.SubElement(s, "course_id").text = str(r[5])

        return make_response(
            ET.tostring(root),
            200,
            {"Content-Type": "application/xml"}
        )

    return jsonify([
        {
            "id": r[0],
            "first_name": r[1],
            "last_name": r[2],
            "age": r[3],
            "gender": r[4],
            "course_id": r[5]
        } for r in rows
    ]), 200


# UPDATE
@students_bp.route("/student/<int:id>", methods=["PUT"])
@token_required
def update_student(id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE student
        SET first_name=%s, last_name=%s, age=%s, gender=%s, Course_idCourse=%s
        WHERE idStudent=%s
        """,
        (
            data["first_name"],
            data["last_name"],
            data["age"],
            data["gender"],
            data["course_id"],
            id
        )
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Student updated"}), 200

# DELETE
@students_bp.route("/student/<int:id>", methods=["DELETE"])
@token_required
def delete_student(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE idStudent=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Student deleted"}), 200


# SEARCH
@students_bp.route("/student/search", methods=["GET"])
def search_student():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Name query required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM student
        WHERE first_name LIKE %s OR last_name LIKE %s
        """,
        (f"%{name}%", f"%{name}%")
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {
            "id": r[0],
            "first_name": r[1],
            "last_name": r[2],
            "age": r[3],
            "gender": r[4],
            "course_id": r[5]
        } for r in rows
    ]), 200
