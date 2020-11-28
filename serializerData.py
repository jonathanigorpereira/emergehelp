from marshmallow import fields, validates, ValidationError
from flask_marshmallow import Marshmallow
from model import Datas
from werkzeug.security import generate_password_hash, check_password_hash

ma = Marshmallow()


def configure(app):
    ma.init_app(app)


def __init__(self, id_user, date, id_category, data):
    self.id_user = Datas.id_user
    self.date = Datas.date
    self.id_category = Datas.id_category
    self.data = Datas.data


class DatasSchema(ma.Schema):
    class Meta:
        Model = Datas

    id = fields.Int()
    id_user = fields.Int(required=True)
    date = fields.Str(required=True)
    id_category = fields.Int(required=True)
    data = fields.Str(required=True)
