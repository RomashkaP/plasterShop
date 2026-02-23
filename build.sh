# Выход при ошибке
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Сбор статических файлов (обязательно для продакшена)
python manage.py collectstatic --no-input

# Главное: применяем миграции базы данных
python manage.py migrate