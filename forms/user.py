from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, \
    TextAreaField, SubmitField, \
    EmailField, BooleanField, \
    TimeField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EditForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    password = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class RecipeForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    ingredients = [BooleanField(text) for text in
                   ["Список с ингредиентами"]]
    cooking_time = TimeField('Время приготовления', validators=[DataRequired()])
    content = TextAreaField("Рецепт", validators=[DataRequired()])
    is_private = BooleanField('Личное')
    image = FileField('Изображение', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')
