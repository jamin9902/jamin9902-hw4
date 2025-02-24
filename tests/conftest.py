import pytest
import sqlite3
import os

@pytest.fixture(scope="session")
def test_db():
    """Create a test database and populate it with test data"""
    # Create test database in memory
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_data.db')
    conn = sqlite3.connect(db_path)
    
    # Create tables
    conn.execute('''
        CREATE TABLE IF NOT EXISTS zip_county (
            zip TEXT,
            county_code TEXT
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS county_health_rankings (
            fipscode TEXT,
            measure_name TEXT,
            value REAL,
            state TEXT,
            county TEXT
        )
    ''')
    
    # Insert test data
    conn.execute("INSERT INTO zip_county VALUES ('02138', '25017')")  # Cambridge, MA
    conn.execute("""
        INSERT INTO county_health_rankings 
        VALUES ('25017', 'Adult obesity', 22.5, 'Massachusetts', 'Middlesex County')
    """)
    
    conn.commit()
    conn.close()
    
    yield db_path
    
    # Cleanup after tests
    os.remove(db_path)
