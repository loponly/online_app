from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import timedelta
from dotenv import load_dotenv
import os
from functools import wraps

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///local_cache.db')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1)))
cachedb = SQLAlchemy(app)
jwt = JWTManager(app)

# Define models
class Business(cachedb.Model):  # Updated to use cachedb
    id = cachedb.Column(cachedb.Integer, primary_key=True)
    name = cachedb.Column(cachedb.String(80), nullable=False)
    is_approved = cachedb.Column(cachedb.Boolean, default=False)
    # Add more fields as necessary

class Project(cachedb.Model):  # Updated to use cachedb
    id = cachedb.Column(cachedb.Integer, primary_key=True)
    business_id = cachedb.Column(cachedb.Integer, cachedb.ForeignKey('business.id'), nullable=False)
    title = cachedb.Column(cachedb.String(120), nullable=False)
    students = cachedb.relationship('Student', secondary='project_student', backref='projects')
    # Add more fields as necessary

class Student(cachedb.Model):  # Updated to use cachedb
    id = cachedb.Column(cachedb.Integer, primary_key=True)
    name = cachedb.Column(cachedb.String(80), nullable=False)
    reward_points = cachedb.Column(cachedb.Integer, default=0)
    # Add more fields as necessary

project_student = cachedb.Table('project_student',  # Updated to use cachedb
    cachedb.Column('project_id', cachedb.Integer, cachedb.ForeignKey('project.id'), primary_key=True),
    cachedb.Column('student_id', cachedb.Integer, cachedb.ForeignKey('student.id'), primary_key=True)
)

def is_local_request():
    return request.remote_addr in ['127.0.0.1', '::1', 'localhost']

def jwt_required_if_not_local():
    def wrapper(fn):
        @wraps(fn)  # Ensure the wrapper function has the same name and docstring as the original function
        def decorated_function(*args, **kwargs):
            if not is_local_request():
                return jwt_required()(fn)(*args, **kwargs)
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper

@app.before_request
def check_authentication():
    if is_local_request():
        # Skip authentication for local requests
        return
    # ... existing authentication logic ...

@app.route('/register_business', methods=['POST'])
def register_business():
    data = request.json
    new_business = Business(name=data['name'])
    cachedb.session.add(new_business)  # Updated to use cachedb
    cachedb.session.commit()  # Updated to use cachedb
    return jsonify({"message": "Business registered successfully"}), 201

@app.route('/post_project', methods=['POST'])
@jwt_required_if_not_local()
def post_project():
    data = request.json
    new_project = Project(business_id=data['business_id'], title=data['title'])
    cachedb.session.add(new_project)  # Updated to use cachedb
    cachedb.session.commit()  # Updated to use cachedb
    return jsonify({"message": "Project posted successfully"}), 201

@app.route('/register_student', methods=['POST'])
def register_student():
    data = request.json
    new_student = Student(name=data['name'])
    cachedb.session.add(new_student)  # Updated to use cachedb
    cachedb.session.commit()  # Updated to use cachedb
    return jsonify({"message": "Student registered successfully"}), 201

@app.route('/mark_attendance', methods=['POST'])
@jwt_required_if_not_local()
def mark_attendance():
    data = request.json
    project = Project.query.get(data['project_id'])
    student = Student.query.get(data['student_id'])
    
    if not project or not student:
        return jsonify({"error": "Project or Student not found"}), 404
    
    if student not in project.students:
        project.students.append(student)
        cachedb.session.commit()  # Updated to use cachedb
    
    return jsonify({"message": "Attendance marked successfully"}), 200

@app.route('/update_profile', methods=['POST'])
@jwt_required_if_not_local()
def update_profile():
    data = request.json
    student = Student.query.get(data['student_id'])
    
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    # Update student profile with project data
    student.reward_points += data.get('reward_points', 0)
    # Add more updates as necessary
    
    cachedb.session.commit()  # Updated to use cachedb
    return jsonify({"message": "Profile updated successfully"}), 200

@app.route('/approve_business', methods=['POST'])
@jwt_required_if_not_local()
def approve_business():
    data = request.json
    business = Business.query.get(data['business_id'])
    if not business:
        return jsonify({"error": "Business not found"}), 404
    
    business.is_approved = True
    cachedb.session.commit()  # Updated to use cachedb
    return jsonify({"message": "Business approved successfully"}), 200

@app.route('/join_project', methods=['POST'])
def join_project():
    data = request.json
    project_id = data.get('project_id')
    student_id = data.get('student_id')
    # Logic to add student to project
    # ...
    return jsonify({'message': 'Student joined project successfully'})

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    project_id = data.get('project_id')
    user_id = data.get('user_id')
    content = data.get('content')
    # Logic to save feedback
    # ...
    return jsonify({'message': 'Feedback submitted successfully'})

@app.route('/view_attendance', methods=['GET'])
def view_attendance():
    user_id = request.args.get('user_id')
    # Logic to retrieve attendance
    # ...
    return jsonify({'attendance': []})

if __name__ == '__main__':
    app.run(debug=True)
