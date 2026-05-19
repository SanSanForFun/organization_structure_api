#!/bin/bash
echo "Ожидание базы данных..."

while ! python -c "import psycopg2; psycopg2.connect(host='db', port=5432, user='$DATABASE_USER', password='$DATABASE_PASSWORD', dbname='$DATABASE_NAME')" 2>/dev/null; do
    echo "База данных не готова, пробуем через 2 секунды..."
    sleep 2
done

echo "База данных подключена!"
echo "Применение миграций..."
python manage.py migrate --noinput

echo "Запуск сервера..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2