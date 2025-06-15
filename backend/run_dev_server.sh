#!/bin/bash

if [ -f .env ]; then
  echo "Using .env file"
  set -a
  source .env
fi

if [ -d venv ]; then
  echo "Using venv"
  source "venv/bin/activate"
  python3 --version
fi

python3 manage.py migrate

if [ ! -d static_backend ]; then
  python3 manage.py collectstatic
  mkdir -p "static_backend/media"
fi


echo "Загрузка ингредиентов"
python3 load_ingredients.py && echo "Ok" || echo "НЕ УДАЛОСЬ"

if [[ "${DEMO_DATA}" == "1" ]]; then
  echo "Загрузка тестовых данных"
  python3 create_test_data.py && echo "Ok" || echo "НЕ УДАЛОСЬ"
fi

echo "Запуск сервера..."
echo "Debug: $DEBUG"

if [ -z "$DEBUG" ] || [ "$DEBUG" -eq 1 ] ; then
  python3 manage.py runserver "0:8000"
else
  python3 -m gunicorn --bind "0.0.0.0:8000" backend.wsgi
fi
