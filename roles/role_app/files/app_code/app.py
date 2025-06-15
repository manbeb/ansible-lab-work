import sys
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Получаем название окружения из переменной окружения
# Если переменная не задана, используем "unknown"
environment = os.environ.get('APP_ENVIRONMENT', 'unknown')

# Добавляем чтение новой переменной
ip_address = os.environ.get('APP_IP_ADDRESS', 'not_set')

@app.route('/')
# ... (эта функция без изменений)

@app.route('/api/status')
def status():
    return jsonify({
        "status": "OK",
        "environment": environment,
        "ip_address": ip_address  # <--- ДОБАВЛЯЕМ НОВОЕ ПОЛЕ В ОТВЕТ
    })
# конец

if __name__ == '__main__':
    # Получаем порт из переменной окружения APP_PORT.
    # Если она не задана, используем 5000 по умолчанию.
    # int() важен, т.к. переменные окружения - это строки.
    port = int(os.environ.get('APP_PORT', 5000))
    # Слушаем на всех интерфейсах (0.0.0.0) и на НАСТРАИВАЕМОМ порту
    app.run(host='0.0.0.0', port=port)
