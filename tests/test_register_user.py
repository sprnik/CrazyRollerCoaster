import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os

# Добавление путей к модулям
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from datetime import datetime
from admin.orm.models import db, User, Visitor, Ticket, Visit
from common.common_orm import register_user, delete_visitor as delete_visitor_orm
from common.common_sql import delete_visitor as delete_visitor_sql
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register_user(client):
    with app.app_context():
        username = "testuser"
        email = "testuser@example.com"
        password = "testpassword"
        date_of_birth = "1990-01-01"

        response = register_user(username, email, password, date_of_birth)
        assert response == "User registered successfully"

        # Проверяем, что пользователь был добавлен в таблицу User
        user = User.query.filter_by(email=email).first()
        assert user is not None
        assert user.username == username

        # Проверяем, что посетитель был добавлен в таблицу Visitor
        visitor = Visitor.query.filter_by(email=email).first()
        assert visitor is not None
        assert visitor.name == username
        assert visitor.date_of_birth == datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        assert visitor.is_adult == True

def test_register_user_existing_email(client):
    with app.app_context():
        username = "testuser"
        email = "testuser@example.com"
        password = "testpassword"
        date_of_birth = "1990-01-01"

        # Регистрируем пользователя первый раз
        response = register_user(username, email, password, date_of_birth)
        assert response == "User registered successfully"

        # Пытаемся зарегистрировать пользователя с тем же email второй раз
        response = register_user(username, email, password, date_of_birth)
        assert response == "A user with this email already exists."

def test_delete_nonexistent_visitor_orm(client):
    with app.app_context():
        # Попытка удаления несуществующего посетителя
        response = delete_visitor_orm(9999)  # ID, который не существует
        assert response == "Visitor not found"

def test_delete_nonexistent_visitor_sql(client):
    with app.app_context():
        # Попытка удаления несуществующего посетителя
        response = delete_visitor_sql(9999)  # ID, который не существует
        assert response == "Visitor not found"
