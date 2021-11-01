
import pytest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import Products




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
