from flask import Blueprint, request, jsonify
import jwt
from db import get_connection
from datetime import datetime, timedelta
from functools import wraps


SECRET_KEY = "CSelect1"
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password required"}), 400

    username = data["username"]
    password = data["password"]

    # Check credentials in the database
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # Generate JWT token
    token = jwt.encode(
        {"user_id": user[0], "exp": datetime.utcnow() + timedelta(hours=2)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated