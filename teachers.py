from flask import Blueprint, request, jsonify
from db import get_connection
from auth import token_required

teachers_bp = Blueprint("teachers", __name__)


# CREATE TEACHER

@teachers_bp.route("/teacher", methods=["POST"])
@token_required
def create_teacher():
    data = request.json

    if not data or "first_name" not in data or "last_name" not in data:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO teacher (first_name, last_name)
        VALUES (%s, %s)
        """,
        (data["first_name"], data["last_name"])
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Teacher created"}), 201



# READ ALL TEACHERS

@teachers_bp.route("/teachers", methods=["GET"])
def get_teachers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM teacher")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {
            "idTeacher": r[0],
            "first_name": r[1],
            "last_name": r[2]
        } for r in rows
    ]), 200



# UPDATE TEACHER

@teachers_bp.route("/teacher/<int:id>", methods=["PUT"])
@token_required
def update_teacher(id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE teacher
        SET first_name=%s, last_name=%s
        WHERE idTeacher=%s
        """,
        (data["first_name"], data["last_name"], id)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Teacher updated"}), 200



# DELETE TEACHER

@teachers_bp.route("/teacher/<int:id>", methods=["DELETE"])
@token_required
def delete_teacher(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM teacher WHERE idTeacher=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Teacher deleted"}), 200



# SEARCH TEACHER

@teachers_bp.route("/teacher/search", methods=["GET"])
def search_teacher():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Name query required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM teacher
        WHERE first_name LIKE %s OR last_name LIKE %s
        """,
        (f"%{name}%", f"%{name}%")
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {
            "idTeacher": r[0],
            "first_name": r[1],
            "last_name": r[2]
        } for r in rows
    ]), 200
