from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.api.app import create_app
from src.persistence.session import init_db


@pytest.fixture()
def app():
    init_db()
    return create_app()


@pytest.fixture()
def client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def temp_db(tmp_path: Path):
    return tmp_path / "test.db"
