from flask import Flask, render_template
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///condition_monitor.db"
app.config["SECRET_KEY"] = "97fdf98cb2f69976dc8c7c17"
bcrypt = Bcrypt(app)

from condition_monitor import routes