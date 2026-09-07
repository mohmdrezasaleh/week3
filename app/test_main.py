from app.main import app
from unittest.mock import MagicMock,patch
from fastapi.testclient import TestClient

#connect to main.py as client
client = TestClient(app)


#checking parameters of check function
def test_status():
    respone = client.get("/status")

    assert respone.status_code = 200

    data = respone.json()
#checking fields of status result
    assert "cpu_percent" in data
    assert "ram_percent" in data
    assert "hostname" in data

#checking data type
    assert isinstance(data["cpu_percent"], (int, float))
    assert isinstance(data["ram_percent"], (int, float))
    assert isinstance(data["hostname"], str)    

#checking int values in percent
    assert 0 <= data["cpu_percent"] <= 100
    assert 0 <= data["ram_percent"] <= 100

#hostname shouldn't be empty
    assert data["hostname"] != ""




@patch("app.main.database")
def test_visit(mock_database: MagicMock):
    mock_database.incr.return_value = 1

    resposne = client.post("/visit")

    assert resposne.status_code == 200

    data = resposne.json()

    assert "visits" in data
    assert data["visits"] == 1

    mock_database.incr.assert_called_one_with("visits")

@patch("app.main.database")
def test_visit_redis_failure(mock_database: MagicMock):

    mock_database.incr.side_effect = redis.RedisError(
        "Redis Unavailable !"
    )

    try:
        client.post("/visit")
    except redis.RedisError:
        pass

    mock_database.incr.assert_called_once_with("visits")