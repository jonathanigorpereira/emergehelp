from marshmallow import fields, validates, ValidationError
from flask_marshmallow import Marshmallow
from model import Users
from werkzeug.security import generate_password_hash, check_password_hash

ma = Marshmallow()


def configure(app):
    ma.init_app(app)


def __init__(self, first_name, last_name, birthday, email, password, aditional_infos):
    self.first_name = Users.first_name
    self.last_name = Users.last_name
    self.birthday = Users.birthday
    self.email = Users.email
    self.password = Users.password
    self.aditional_infos = Users.aditional_infos


class UsersSchema(ma.Schema):
    class Meta:
        Model = Users

    id = fields.Int()
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    birthday = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    aditional_infos = fields.Str(required=True)
