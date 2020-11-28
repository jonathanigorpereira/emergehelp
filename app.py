import os
from users import bp_users
from flask import Flask, render_template, redirect, url_for, session
from flask_migrate import Migrate
from model import configure as configure_db, Users, Datas
from serializerUser import configure as configure_ma
from serializerData import configure as configure_ma_data
from flask_sqlalchemy import SQLAlchemy
import flask_login as flasklogin
from flask_login import UserMixin, login_user, LoginManager
from datetime import timedelta
from random import random


db = SQLAlchemy()

app = Flask(__name__)

random()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Caneta21*@localhost:3306/api_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'testechavesecreta'
app.permanent_session_lifetime = timedelta(minutes=10)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

# configura o banco de dados
configure_db(app)
# configura o serializer
configure_ma(app)
configure_ma_data(app)
# configura a migração do banco
Migrate(app, app.db)

# registra as blueprints, que são as conexões das rotas da api
app.register_blueprint(bp_users)


@app.route('/protect')
@flasklogin.login_required
def protect():
    return render_template('protected.html')


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()


@app.route("/")
def index():
    return redirect(url_for('users.login'))
    return render_template('login.html')


if __name__ == "__main__":
    app.run()
