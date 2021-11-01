import pytest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import Products, app


@pytest.fixture
def flask_app_mock():
    app_mock = app
    db = SQLAlchemy(app_mock)
    db.init_app(app_mock)
    return app_mock


@pytest.fixture
def api_mock():
    api_products = Products (
        name='Potato',
        arrival_date='12.07.1995',
        category='Vegies',
        country='UA',
        price='20',
    )
    return api_products


@pytest.fixture
def mock_get_sqlalchemy(mocker):
    mock = mocker.patch("flask_sqlalchemy._QueryProperty.__get__").return_value = mocker.Mock()
    return mock