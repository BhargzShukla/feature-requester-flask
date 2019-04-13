from feature_requester_app import app as app
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy(app)


class FeatureRequest(db.Model):
    u"""
    Table structure definition for feature requests.
    """
    __tablename__ = 'feature_request'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    client_id = db.Column(
        db.Integer,
        db.ForeignKey('client.id'),
        nullable=False
    )
    client = db.relationship('Client', backref='feature_request')
    client_priority = db.Column(db.Integer, default=1)

    product_area_id = db.Column(
        db.Integer,
        db.ForeignKey('product_area.id'),
        nullable=False
    )
    product_area = db.relationship('ProductArea', backref='feature_request')

    target_date = db.Column(db.Date, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __repr__(self):
        return '%r' % self.title

    __str__ = __repr__


class Client(db.Model):
    u"""
    Table structure definition for clients.
    """
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '%r' % self.name

    __str__ = __repr__


class ProductArea(db.Model):
    u"""
    Table structure definition for product areas.
    """
    __tablename__ = 'product_area'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '%r' % self.name

    __str__ = __repr__
