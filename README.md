# TankWorld — лабораторная работа №1 (DevOps, CI/CD)

Backend: Django + Django REST Framework (SQLite)
Frontend: Vue 3 + Vite

## Запуск backend локально

    cd backend
    python -m venv venv
    venv\Scripts\activate        # Windows
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

API: http://127.0.0.1:8000/api/  (танки, игроки, кланы, карты, бои, достижения)

## Запуск тестов

    cd backend
    pytest
