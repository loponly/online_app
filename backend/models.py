from backend.app import cachedb  # Updated to import cachedb

# Association table for many-to-many relationship
project_student = cachedb.Table('project_student',  # Updated to use cachedb
    cachedb.Column('project_id', cachedb.Integer, cachedb.ForeignKey('project.id'), primary_key=True),
    cachedb.Column('student_id', cachedb.Integer, cachedb.ForeignKey('student.id'), primary_key=True)
)

class Business(cachedb.Model):  # Updated to use cachedb
    id = cachedb.Column(cachedb.Integer, primary_key=True)
    name = cachedb.Column(cachedb.String(100), nullable=False)
    projects = cachedb.relationship('Project', backref='business', lazy=True)

class Project(cachedb.Model):  # Updated to use cachedb
    id = cachedb.Column(cachedb.Integer, primary_key=True)
    title = cachedb.Column(cachedb.String(100), nullable=False)
    business_id = cachedb.Column(cachedb.Integer, cachedb.ForeignKey('business.id'), nullable=False)
    students = cachedb.relationship('Student', secondary=project_student, lazy='subquery',
                               backref=cachedb.backref('projects', lazy=True))

class Student(cachedb.Model):  # Updated to use cachedb
    id = cachedb.Column(cachedb.Integer, primary_key=True)
    name = cachedb.Column(cachedb.String(100), nullable=False)
    # Add more fields as necessary

class Feedback(cachedb.Model):
    id = cachedb.Column(cachedb.Integer, primary_key=True)
    user_id = cachedb.Column(cachedb.Integer, cachedb.ForeignKey('user.id'), nullable=False)
    project_id = cachedb.Column(cachedb.Integer, cachedb.ForeignKey('project.id'), nullable=False)
    content = cachedb.Column(cachedb.Text, nullable=False)
    # ... other fields ...

class Attendance(cachedb.Model):
    id = cachedb.Column(cachedb.Integer, primary_key=True)
    user_id = cachedb.Column(cachedb.Integer, cachedb.ForeignKey('user.id'), nullable=False)
    project_id = cachedb.Column(cachedb.Integer, cachedb.ForeignKey('project.id'), nullable=False)
    date = cachedb.Column(cachedb.Date, nullable=False)
    # ... other fields ...
