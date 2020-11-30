from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from datetime import datetime
# instância do banco
db = SQLAlchemy()


# inicializa as configurações do banco
def configure(app):
    db.init_app(app)
    app.db = db


# criando a classe/Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    birthday = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), unique=False)
    aditional_infos = db.Column(db.String(255))
    datas = db.relationship('Datas', backref='_user')


class Datas(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey(Users.id), unique=False)
    date = db.Column(
        db.String(255), default=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    id_category = db.Column(db.Integer, unique=False)
    data = db.Column(db.String(255), nullable=False)
