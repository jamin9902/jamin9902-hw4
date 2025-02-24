import pytest
from api.app import app
import json
import os

@pytest.fixture
def client(test_db):
    app.config['TESTING'] = True
    app.config['DATABASE'] = test_db
    with app.test_client() as client:
        yield client

def test_valid_request(client):
    """Test a valid request with existing zip code and measure"""
    data = {
        'zip': '02138',
        'measure_name': 'Adult obesity'
    }
    response = client.post('/county_data', json=data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert isinstance(response_data, list)
    if len(response_data) > 0:
        assert 'measure_name' in response_data[0]
        assert 'value' in response_data[0]

def test_invalid_zip_code(client):
    """Test with invalid zip code format"""
    data = {
        'zip': '123',  # Invalid zip code (too short)
        'measure_name': 'Adult obesity'
    }
    response = client.post('/county_data', json=data)
    assert response.status_code == 400
    assert b'Invalid zip code format' in response.data

def test_invalid_measure_name(client):
    """Test with invalid measure name"""
    data = {
        'zip': '02138',
        'measure_name': 'Invalid Measure'
    }
    response = client.post('/county_data', json=data)
    assert response.status_code == 400
    assert b'Invalid measure_name' in response.data

def test_missing_fields(client):
    """Test with missing required fields"""
    data = {'zip': '02138'}  # Missing measure_name
    response = client.post('/county_data', json=data)
    assert response.status_code == 400
    assert b'Both zip and measure_name are required' in response.data

def test_teapot_easter_egg(client):
    """Test the teapot easter egg"""
    data = {
        'zip': '02138',
        'measure_name': 'Adult obesity',
        'coffee': 'teapot'
    }
    response = client.post('/county_data', json=data)
    assert response.status_code == 418

def test_nonexistent_endpoint(client):
    """Test accessing a non-existent endpoint"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert b'Endpoint not found' in response.data
