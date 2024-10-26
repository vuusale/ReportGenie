from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///findings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Association Table for Many-to-Many Relationship
project_vulnerabilities = db.Table('project_vulnerabilities',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.project_id'), primary_key=True),
    db.Column('vulnerability_id', db.Integer, db.ForeignKey('vulnerabilities.vulnerability_id'), primary_key=True)
)

class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    reporter_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    end_date = db.Column(db.String(50), nullable=True)
    executive_summary = db.Column(db.Text, nullable=True)
    vuln_count = db.Column(db.Integer, nullable=True)
    vulnerabilities = db.relationship('Vulnerability', secondary=project_vulnerabilities, backref=db.backref('projects', lazy=True))

class Vulnerability(db.Model):
    __tablename__ = 'vulnerabilities'

    vulnerability_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    vulnerability_name = db.Column(db.String(150), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    vulnerable_component = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    impact = db.Column(db.Text, nullable=True)
    remediation = db.Column(db.Text, nullable=True)
    poc = db.Column(db.Text, nullable=True)

class CustomField(db.Model):
    __tablename__ = 'custom_fields'
    
    custom_field_id = db.Column(db.Integer, primary_key=True)
    custom_field_name = db.Column(db.String(100), nullable=False)
    custom_field_content = db.Column(db.Text, nullable=True)

if not os.path.exists('./reportGenie.db'):
    with app.app_context():
        db.create_all()