from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, login_manager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    ENV = "prd"

    if ENV == "dev":
        app.debug = True
        app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgrepba6ikha-@localhost/flaskapp'

    else:
        app.debug = False
        app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://euxwieiklbgchh:e00ad230c19ff4480182593902d73fd637beec3e305050f77d15160aa4fdedf3@ec2-54-217-15-9.eu-west-1.compute.amazonaws.com:5432/d43llm3tjc9p51'

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  
    app.config["SECRET_KEY"] = "KKKJ7878bhjbnbh8787"
    db.init_app(app)



    from .views import views
    from .auth import auth

    #prefix will be adde before what comes from imports
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")


    from .models import User, Note

    create_database(app)


    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app

def create_database(app):
    if not os.path.exists("website/"+"initalDb"):
        os.mkdir("website/"+"initalDb")
        db.create_all(app=app)
        print("Database created!")

