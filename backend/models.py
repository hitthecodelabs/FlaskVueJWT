# models.py

from extensions import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    company_name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    api_key = db.Column(db.String(255), nullable=True)
    jira_domain = db.Column(db.String(255), nullable=True)
    jira_email = db.Column(db.String(255), nullable=True)
