# Выход при ошибке
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Сбор статических файлов (обязательно для продакшена)
python manage.py collectstatic --no-input

# Главное: применяем миграции базы данных
python manage.py migrate

# Создание суперпользователя (только если указана переменная CREATE_SUPERUSER)
if [[ $CREATE_SUPERUSER]]; then
echo 'Creating superuser...'
python manage.py createsuperuser --no-input
echo 'Superuser created successfully!'
fi