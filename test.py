import pytest
from fastapi.testclient import TestClient
from Api import app  # Import your FastAPI app test 4

client = TestClient(app)

@pytest.mark.parametrize("number,expected", [
    (1, {"is_prime": False}),
    (2, {"is_prime": True}),
    (3, {"is_prime": True}),
    (4, {"is_prime": False}),
    (5, {"is_prime": True}),
    (10, {"is_prime": False}),
    (13, {"is_prime": True}),
    (17, {"is_prime": True}),
    (19, {"is_prime": True}),
    (20, {"is_prime": False}),
])
# Test case 1: Kiểm tra route /get_version trả về phiên bản đúng
def test_get_version():
    response = client.get("/get_version")
    assert response.status_code == 200
    assert response.json() == {"version": "1.0"}

