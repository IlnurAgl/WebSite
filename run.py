from main import create_app
# Запуск WebServer

app = create_app()  # Создание приложения

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
