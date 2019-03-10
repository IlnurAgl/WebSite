# Файл с конфигурациями сервера
import os


# Основные конфигурации пользователя
class Config:
    SECRET_KEY = 'VerySecretKey'  # Секретный ключ
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Подключение базы данных
    MAIL_SERVER = 'smtp.googlemail.com'  # Адрес почты
    MAIL_PORT = 587  # Порт для отправки
    MAIL_USE_TLS = True  # Активирование TLS
    MAIL_USE_SSL = False  # Отключение SSL
    MAIL_USERNAME = 'ilnur5247@gmail.com'  # Логин от почты
    MAIL_PASSWORD = ''  # Пароль от почты
