import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dbblog.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lisen1018@127.0.0.1:3306/myapp/?charset=utf8'
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SRF_ENABLED'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

lm = LoginManager()
# lm.setup_app(app)  #
lm.init_app(app)
lm.login_view = 'login'

from myapp import views, models
