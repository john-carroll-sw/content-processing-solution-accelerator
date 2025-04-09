import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from src.ContentProcessorAPI.app.dependencies import get_token_header, get_query_token
# from starlette.status import HTTP_400_BAD_REQUEST


@pytest.fixture
def test_app():
    app = FastAPI()

    @app.get("/header-protected")
    async def protected_route_header(dep=Depends(get_token_header)):
        return {"message": "Success"}

    @app.get("/query-protected")
    async def protected_route_query(dep=Depends(get_query_token)):
        return {"message": "Success"}

    return app


def test_get_token_header_fails(test_app):
    client = TestClient(test_app)
    # Provide the required header so FastAPI doesn't return 422
    response = client.get("/header-protected", headers={"x-token": "fake"})
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}


def test_get_query_token_fails(test_app):
    client = TestClient(test_app)
    # Provide the required query param so FastAPI doesn't return 422
    response = client.get("/query-protected?token=fake")
    assert response.status_code == 400
    assert response.json() == {"detail": "No ... token provided"}
