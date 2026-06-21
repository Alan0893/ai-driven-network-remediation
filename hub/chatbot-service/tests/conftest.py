import pytest
from fastapi.testclient import TestClient

from chatbot_service import app


@pytest.fixture()
def client():
    return TestClient(app)
