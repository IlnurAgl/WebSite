from flask import Blueprint, render_template
# Файл для возврата страницы при ошибке

errors = Blueprint('errors', __name__)


#Обработка ошибки 404
@errors.app_errorhandler(404)
def error_404(error):
	return render_template('errors/404.html'), 404


#Обработка ошибки 403
@errors.app_errorhandler(403)
def error_403(error):
	return render_template('errors/403.html'), 403


#Обработка ошибки 500
@errors.app_errorhandler(500)
def error_500(error):
	return render_template('errors/500.html'), 500
