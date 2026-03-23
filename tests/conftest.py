import pytest
import sys
import os

# Add project root to path if needed (pytest usually handles this if run from root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.database import init_db, SessionLocal, engine
from data.models import Base

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Ensure database is initialized for the test session."""
    init_db()
    yield
    # Optional: cleanup or leave it if using a separate test.db

@pytest.fixture
def db_session():
    """Provides a clean database session for tests."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
