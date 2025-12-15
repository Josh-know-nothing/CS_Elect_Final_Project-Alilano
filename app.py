from flask import Flask
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root",
    database="mydb"
)

@app.route("/")
def home():
    return "connected!"

if __name__ == "__main__":
    app.run(debug=True)
