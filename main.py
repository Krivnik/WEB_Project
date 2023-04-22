from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from data import db_session
from data.users import User
from data.recipes import Recipe
from forms.user import RegisterForm, LoginForm, EditForm, RecipeForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
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


@app.route('/recipes', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        rs = db_sess.query(Recipe).all()
        n = '1' if not rs else str(int(rs[-1].id) + 1)
        img_name = 'static/img/' + n + '.' + request.files['image'].filename.rsplit('.')[-1]
        request.files['image'].save(img_name)
        recipe = Recipe(
            title=form.title.data,
            # ingredients=form.ingredients.data,
            cooking_time=form.cooking_time.data.isoformat(timespec='minutes'),
            content=form.content.data,
            image=img_name,
            is_private=form.is_private.data)
        current_user.recipes.append(recipe)
        db_sess.merge(current_user)
        db_sess.commit()
        # Я знаю об этой ошибке, но пока не смог ее пофиксить
        return redirect('/')
    return render_template('recipe.html', title='Добавление рецепта', form=form)


@app.route('/recipes/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    form = RecipeForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        recipe = db_sess.query(Recipe).filter(Recipe.id == id, Recipe.user == current_user).first()
        if recipe:
            form.title.data = recipe.title
            # form.ingredients.data = recipe.ingredients
            form.cooking_time.data = datetime.time(recipe.cooking_time.split(':'))
            form.content.data = recipe.content
            form.is_private.data = recipe.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        recipe = db_sess.query(Recipe).filter(Recipe.id == id, Recipe.user == current_user).first()
        img_name = recipe.image.rsplit('.')[0] + '.' \
                   + request.files['image'].filename.rsplit('.')[-1]
        request.files['image'].save(img_name)
        if recipe:
            recipe.title = form.title.data
            # recipe.ingredients = form.ingredients.data
            recipe.cooking_time = form.cooking_time.data.isoformat(timespec='minutes')
            recipe.content = form.content.data
            recipe.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('recipe.html', title='Редактирование рецепта', form=form)


@app.route('/recipes_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def recipe_delete(id):
    db_sess = db_session.create_session()
    recipe = db_sess.query(Recipe).filter(Recipe.id == id, Recipe.user == current_user).first()
    if recipe:
        db_sess.delete(recipe)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


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


def main():
    db_session.global_init("db/recipes.db")
    app.run()


if __name__ == '__main__':
    main()
