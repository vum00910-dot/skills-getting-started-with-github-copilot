import pytest
from copy import deepcopy
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory `activities` state before/after each test."""
    original = deepcopy(activities)
    try:
        yield
    finally:
        activities.clear()
        activities.update(original)
