from flask import Blueprint, redirect, request, abort
from flask import render_template, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from main import db, bcrypt
from main.models import User, Post
from main.users.forms import RegistrationForm, LoginForm
from main.users.forms import RequestResetForm, ResetPasswordForm
from main.users.forms import UpdateAccountForm
from main.users.utils import save_picture, send_reset_email
# Файл для создания ссылок для пользователя


# Подключение файла
users = Blueprint('users', __name__)

ADMINS = ['11']


# Сайт для регистрации
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user = User(username=form.username.data, email=form.email.data,
                        image_file=picture_file, password=hashed_password)
        else:
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт создан! Вы можете войти в него', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Регистрация', form=form)


# Сайт для авторизации пользователя
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Ошибка входа. Проверьте адрес почты и пароль', 'danger')
    return render_template('login.html', title='Авторизация', form=form)


# Выход из аккаунта
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# Сайт с информации о пользователи
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    if str(current_user.id) in ADMINS:
        return render_template('account.html', title='Аккаунт',
         image_file=image_file, form=form, admin=True)
    else:
        return render_template('account.html', title='Аккаунт',
         image_file=image_file, form=form, admin=False)


# Загрузка информации о пользователи
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user, forUser=True, reverse=False)


@users.route("/user_reverse/<string:username>")
def user_reverse_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user, forUser=True, reverse=True)


# Страница для изменения пароля
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            'На вашу почту было выслано письмо с инструкциями по изменению пароля.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Изменить пароль', form=form)


# Сайт с проверкой запроса
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Неверный запрос', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль измененен! Вы можете войти в аккаунт', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Изменить пароль', form=form)


# Страница для простомотора пользователей для администратора
@users.route('/users_edit')
def users_edit():
    if str(current_user.id) not in ADMINS:
        abort(403)
    else:
        return render_template('users_edit.html', users=User.query.all(), Post=Post)


# Страница для удаления пользователя для администратора
@users.route('/user_del/int:<user_id>')
@login_required
def user_del(user_id):
    if str(current_user.id) not in ADMINS:
        abort(403)
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь удален!', 'success')
    return redirect(url_for('users.users_edit'))
