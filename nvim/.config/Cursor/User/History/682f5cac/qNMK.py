"""
Database connection and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase
import os

# Create the declarative base that all models will inherit from
class Base(DeclarativeBase):
    pass

# Get database path from environment or use default
DB_PATH = os.environ.get('PYDIAL_DB_PATH', 'sqlite:///pydial.db')

# Create engine
engine = create_engine(DB_PATH, echo=False)

# Create session factory
session_factory = sessionmaker(bind=engine)

# Create thread-safe session manager
Session = scoped_session(session_factory)

def init_db():
    """Initialize the database, creating all tables."""
    # Import all models to ensure they're registered with Base
    from . import models
    Base.metadata.create_all(engine)

def get_db_session():
    """Get a new database session.
    
    Returns:
        SQLAlchemy Session: A new database session
    
    Note:
        Remember to close the session when done:
        ```
        session = get_db_session()
        try:
            # do stuff
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        ```
    """
    return Session() 