from flask import render_template, request, Blueprint
from main.models import Post
# Файл с основными ссылками

# Подключение файла
main = Blueprint('main', __name__)


# Основная страница
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, reverse=False, forUser=False)


@main.route('/home_reverse')
def home_reverse():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts, reverse=True, forUser=False)


# Страница о сайте
@main.route("/about")
def about():
    return render_template('about.html', title='О сайте')