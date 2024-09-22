from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    niche = db.Column(db.String(120), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)
    flagged = db.Column(db.Boolean, nullable=False, default=False)

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    industry = db.Column(db.String(60), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)
    flagged = db.Column(db.Boolean, nullable=False, default=False)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(360), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(50), nullable=False)  # e.g., 'public', 'private'
    goals = db.Column(db.Text, nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)
    progress = db.Column(db.Float, nullable=False)
    stat = db.Column(db.String(20), nullable= False, default= "Pending") #Pending, Active, Inactive, Completed
    flagged = db.Column(db.Boolean, nullable=False, default=False)

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    message = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')  # e.g., 'Pending', 'Accepted', 'Rejected'
    negotiation = db.Column(db.Boolean, nullable=False, default=False)
    negotiation_amt = db.Column(db.Float, nullable=False, default = 0)
    for_who = db.Column(db.String(15),nullable=False,default="influencer")
    flagged = db.Column(db.Boolean, nullable=False, default=False)