import pytest
from app import app, find_top_confirmed
import pandas as pd
import folium


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Test if home route returns 200 status code"""
    response = client.get('/')
    assert response.status_code == 200


def test_find_top_confirmed():
    """Test if find_top_confirmed returns correct dataframe"""
    df = find_top_confirmed(n=5)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert 'Confirmed' in df.columns


def test_dataset_exists():
    """Test if dataset file exists and can be loaded"""
    try:
        df = pd.read_csv('static/dataset.csv')
        assert not df.empty
    except FileNotFoundError:
        pytest.fail("Dataset file not found")


def test_map_creation():
    """Test if folium map is created with correct initial parameters"""
    m = folium.Map(
        location=[34.223334, -82.461707],
        tiles='Stamen Toner',
        zoom_start=8
    )
    assert isinstance(m, folium.Map)
    assert m.location == [34.223334, -82.461707]


def test_data_processing():
    """Test if data processing works correctly"""
    corona_df = pd.read_csv('static/dataset.csv')
    by_country = corona_df.groupby('Country_Region').sum()[
        ['Confirmed', 'Deaths', 'Recovered', 'Active']
    ]
    assert isinstance(by_country, pd.DataFrame)
    assert all(col in by_country.columns for col in [
        'Confirmed', 'Deaths', 'Recovered', 'Active'
    ])
