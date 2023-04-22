from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from data import db_session
from data.users import User
from data.recipes import Recipe
from forms.user import RegisterForm, LoginForm, EditForm
from forms.recipe import CreateForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', form=form, message="Неправильный логин или пароль")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if request.method == "GET":
        form.name.data = current_user.name
        form.about.data = current_user.about
    if form.validate_on_submit():

        if not current_user.check_password(form.password.data):
            return render_template('edit.html', title='Редактирование данных', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        user.name = form.name.data
        user.about = form.about.data
        db_sess.commit()
        return redirect('/')
    return render_template('edit.html', title='Редактирование данных', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    return render_template('main_page.html', title='Главная')


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


@app.route('/create')
def create():
    form = CreateForm()
    return render_template('create.html', title='Создание рецепта', form=form)


def main():
    db_session.global_init("db/recipes.db")
    app.run()


if __name__ == '__main__':
    main()
