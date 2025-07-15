"""
Test configuration and fixtures.
"""
import os
import pytest
import tempfile
from database.db import Base, engine

@pytest.fixture(autouse=True)
def test_db():
    """Create a temporary test database."""
    # Create temp db file
    db_fd, db_path = tempfile.mkstemp()
    os.environ['PYDIAL_DB_PATH'] = f'sqlite:///{db_path}'
    
    # Create tables
    Base.metadata.create_all(engine)
    
    yield
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path) 