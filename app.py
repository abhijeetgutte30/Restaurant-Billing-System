from flask import Flask, render_template
from flask_login import login_required

from config import Config, bcrypt, login_manager
from database.database import db
from routes.auth import auth
from routes.menu import menu
from routes.billing import billing
from models.models import Admin, Menu

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(menu)
app.register_blueprint(billing)


# Create Database & Default Admin
with app.app_context():
    db.create_all()

    admin = Admin.query.filter_by(username="admin").first()

    if admin is None:
        admin = Admin(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("✅ Default Admin Created")


# Home Page
@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Restaurant Billing System</title>
        <style>
            body{
                background:#f2f2f2;
                font-family:Arial;
                text-align:center;
                margin-top:100px;
            }

            button{
                padding:15px 35px;
                font-size:20px;
                background:green;
                color:white;
                border:none;
                border-radius:6px;
                cursor:pointer;
            }

            button:hover{
                background:darkgreen;
            }
        </style>
    </head>

    <body>

        <h1>🍽️ Restaurant Billing System</h1>

        <h2 style="color:green;">
            Database Connected Successfully ✅
        </h2>

        <h3>Version 2.0</h3>

        <a href="/login">
            <button>Login</button>
        </a>

    </body>
    </html>
    """


# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    total_menu = Menu.query.count()

    return render_template(
        "dashboard.html",
        total_menu=total_menu
    )


if __name__ == "__main__":
    app.run(debug=True)