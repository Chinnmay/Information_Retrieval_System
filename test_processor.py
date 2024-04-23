import json
import pytest
from processor import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data

def test_process_query_route_valid(client):
    data = {'query': 'test query'}
    response = client.post('/process_query', json=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    assert isinstance(result, list)

def test_process_query_route_invalid(client):
    data = {'invalid_field': 'test query'}
    response = client.post('/process_query', json=data)
    assert response.status_code == 400
    result = json.loads(response.data)
    assert 'error' in result
