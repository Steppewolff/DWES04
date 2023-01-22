import os
from flask import Flask
from flask_login import LoginManager

# Se instancia un objeto de LoginManager
app = Flask(__name__)

app.config['SECRET_KEY'] = 'gomez romano'

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"