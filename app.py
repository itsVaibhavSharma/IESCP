from flask import Flask
from config import Config
from models import db, Admin
from routes import main_bp
import base64

from flask import Flask, session
from flask_session import Session
import redis

app = Flask(__name__)

# Redis configuration
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.StrictRedis(
    host='redis-15695.c232.us-east-1-2.ec2.redns.redis-cloud.com',
    port=15695,
    password='nJieYHXzXDZIoFMuBDP363ENszfiXdDv'  # Replace with your Redis password if one is set
)
app.config['SESSION_PERMANENT'] = False
# app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Set session lifetime (optional)

# Initialize Flask-Session
Session(app)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

    admin = Admin.query.get(1)
    if not admin:
        admin = Admin(email="admin@admin.com", name="Vaibhav Sharma", password="admin")
        db.session.add(admin)
        db.session.commit()
    

@app.template_filter('b64encode')
def b64encode(data):
    return base64.b64encode(data).decode('utf-8')

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
    