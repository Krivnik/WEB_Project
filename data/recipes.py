from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Recipe(SqlAlchemyBase):
    __tablename__ = 'recipes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ingredients = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # потом объясню реализацию
    cooking_time = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # пока пусть строкой будет
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='default.jpg')
    # неполное название загруженного в static/img файла, по умолчанию белая картинка 1х1
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
