from flask import Flask
from config import Config
from models import db, Admin
from routes import main_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

    admin = Admin.query.get(1)
    if not admin:
        admin = Admin(email="admin@admin.com", name="Vaibhav Sharma", password="admin")
        db.session.add(admin)
        db.session.commit()
    

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
    