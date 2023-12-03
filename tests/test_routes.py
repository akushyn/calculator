from app.core.operators import OPERATORS


def test_get_operators(client):
    url = "/api/operators"
    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == list(OPERATORS.keys())
