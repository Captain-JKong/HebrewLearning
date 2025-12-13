"""
Pytest Configuration and Fixtures
Shared test fixtures that can be used across all test files
"""

import pytest
import tempfile
import os
from pathlib import Path

# Add parent directory to path so we can import our modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from database_manager import DatabaseManager
from data_manager import VocabularyManager, ProgressManager
from session_manager import SessionManager
from config import Config


@pytest.fixture
def temp_db_path():
    """Create a temporary database file path"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    yield db_path
    # Cleanup after test
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def database(temp_db_path):
    """Create a fresh database instance with sample data"""
    db = DatabaseManager(temp_db_path)
    db.populate_sample_data()
    yield db
    db.close()


@pytest.fixture
def empty_database(temp_db_path):
    """Create a fresh empty database instance"""
    db = DatabaseManager(temp_db_path)
    yield db
    db.close()


@pytest.fixture
def vocab_manager(database):
    """Create a VocabularyManager with test database"""
    return VocabularyManager(database)


@pytest.fixture
def progress_manager(database):
    """Create a ProgressManager with test database"""
    return ProgressManager(database)


@pytest.fixture
def sample_vocabulary(database):
    """Get sample vocabulary data"""
    return database.get_all_vocabulary()


@pytest.fixture
def session_manager(sample_vocabulary, database):
    """Create a SessionManager with test data"""
    progress = database.get_vocabulary_stats()
    return SessionManager(sample_vocabulary, progress, database)
