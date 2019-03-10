from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from main import db
from main.models import Post
from main.posts.forms import PostForm
# Файл со ссылками для работы с постами

# Подключение файла
posts = Blueprint('posts', __name__)

ADMINS = ['11']

# Сайт для создания нового поста
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост был создан!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='Новый пост',
                           form=form, legend='Новый пост')


# Сайт с информации о посте
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


# Сайт для обновления поста
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Ваш пост был обновлен!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Обновить пост',
                           form=form, legend='Обновить пост')


# Сайт для удаления поста
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост был удален!', 'success')
    return redirect(url_for('main.home'))


@posts.route('/posts_edit')
def posts_edit():
    if str(current_user.id) not in ADMINS:
        abort(403)
    else:
        return render_template('posts_edit.html', posts=Post.query.all())


@posts.route('/post_del/int:<post_id>')
@login_required
def post_del(post_id):
    if str(current_user.id) not in ADMINS:
        abort(403)
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Пост был удален!', 'success')
    return redirect(url_for('posts.posts_edit'))
