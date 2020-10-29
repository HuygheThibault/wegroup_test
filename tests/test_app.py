from __future__ import absolute_import

from app.app import create_app

from starlette.testclient import TestClient
from app.config import Config

app = create_app(Config())
client = TestClient(app)


# INDEX
def test_index_no_params():
    response = client.get("/index")
    assert response.status_code == 200
    assert response.json() == {"index": 132.97}  # may 2020


def test_index_1996():
    response = client.get("/index?year=1996")
    assert response.status_code == 200
    assert response.json() == {"index": 151.28}  # may 2020


def test_index_2013():
    response = client.get("/index?year=2013")
    assert response.status_code == 200
    assert response.json() == {"index": 110.10}  # may 2020


def test_index_2020():
    response = client.get("/index?year=2020")
    assert response.status_code == 400
    assert response.json() == {"detail": "WRONG_YEAR"}


# ZIPCODE
def test_zipcode():
    response = client.get("/zipcode/9000")
    assert response.status_code == 200
    assert response.json() == {"risk_factor": "B"}


def test_zipcode_too_high():
    response = client.get("/zipcode/10000")
    assert response.status_code == 400
    assert response.json() == {"detail": "ZIPCODE_NOT_VALID"}


def test_zipcode_too_low():
    response = client.get("/zipcode/999")
    assert response.status_code == 400
    assert response.json() == {"detail": "ZIPCODE_NOT_VALID"}


def test_zipcode_low_bound():
    response = client.get("/zipcode/9170")
    assert response.status_code == 200
    assert response.json() == {"risk_factor": "A"}


def test_zipcode_high_bound():
    response = client.get("/zipcode/9240")
    assert response.status_code == 200
    assert response.json() == {"risk_factor": "A"}


def test_zipcode_middle():
    response = client.get("/zipcode/9200")
    assert response.status_code == 200
    assert response.json() == {"risk_factor": "A"}
