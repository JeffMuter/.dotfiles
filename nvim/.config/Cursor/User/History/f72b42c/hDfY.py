import os
import tempfile
import pytest
from database import init_db

@pytest.fixture(autouse=True)
def test_db():
    """Create a temporary test database."""
    db_fd, db_path = tempfile.mkstemp()
    os.environ['PYDIAL_DB_PATH'] = f'sqlite:///{db_path}'
    
    yield
    
    os.close(db_fd)
    os.unlink(db_path) 