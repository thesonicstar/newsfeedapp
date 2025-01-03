from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    source_name = db.Column(db.String(100), nullable=True)
    saved_at = db.Column(db.DateTime, default=db.func.current_timestamp())
