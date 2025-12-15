from flask import Flask, jsonify
from students import students_bp
from course import courses_bp
from teachers import teachers_bp  
from auth import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = "CSelect1"

# Blueprints
app.register_blueprint(students_bp, url_prefix='/api')
app.register_blueprint(courses_bp, url_prefix='/api')
app.register_blueprint(teachers_bp, url_prefix='/api') 
app.register_blueprint(auth_bp, url_prefix='/api') 

# routes 
@app.route("/routes")
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "methods": list(rule.methods),
            "url": str(rule)
        })
    return jsonify(routes)

# Root endpoint
@app.route("/")
def index():
    return "Welcome to the Student Management REST API!"

if __name__ == "__main__":
    app.run(debug=True)
