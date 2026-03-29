"""
Database Models for Cashew Disease Detection
"""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Prediction(db.Model):
    """Prediction/Diagnosis model"""
    __tablename__ = 'prediction'
    __table_args__ = (
        db.Index('idx_disease', 'disease'),
        db.Index('idx_created_at', 'created_at'),
        db.Index('idx_disease_date', 'disease', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)

    # Prediction data
    disease = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    cam_path = db.Column(db.String(255), nullable=True)
    segmented_path = db.Column(db.String(255), nullable=True)

    # Probability distribution (stored as JSON string for SQLite compat)
    probabilities = db.Column(db.Text, nullable=True)

    # Metrics
    infection_area = db.Column(db.Float, default=0.0)
    spread_pattern = db.Column(db.String(50), default='Unknown')
    recovery_probability = db.Column(db.Float, nullable=True)

    # Metadata (stored as JSON string for SQLite compat)
    meta = db.Column(db.Text, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Prediction {self.disease} - {self.confidence}%>'


class DiseaseInfo(db.Model):
    """Disease information database"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    scientific_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    symptoms = db.Column(db.Text)
    remediation = db.Column(db.Text)
    severity = db.Column(db.String(20))

    def __repr__(self):
        return f'<DiseaseInfo {self.name}>'
