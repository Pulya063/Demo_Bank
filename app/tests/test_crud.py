from datetime import datetime, date

import pytest

from confest import *

URL = "/bank"
del_aid = "13ddb818-10cd-4f61-9283-7b61d5dafbf7"
aid = "ba94cef8-047d-45c0-bef6-c92d4e9e7bc4"

# def test_create_account(client):
#     data = {
#         "name": "John",
#         "surname": "Doe",
#         "birth_date": "2000-01-01",
#         "transactions": []
#     }
#     response = client.post(f"{URL}/", json=data)
#     assert response.status_code == 200, f"Unexpected status code: {response.status_code}, response: {response.json()}"
#     result = response.json()
#     assert result["name"] == "John"
#     assert "id" in result
#     print(result)

# def test_get_account(client):
#     response = client.get(f"{URL}/account/{aid}")
#     assert response.status_code == 200, f"Unexpected status code: {response.status_code}, response: {response.json()}"
#     result = response.json()
#     print(result)

@pytest.mark.order(1)
def test_get_all_accounts(client):
    response = client.get(f"{URL}/")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, response: {response.json()}"
    result = response.json()
    print(result)

# def test_update_account(client):
#     info = {
#         "name": "John",
#         "surname": "Doe",
#         "birth_date": "2022-01-01",
#         "balance": [],
#         "transactions": []
#     }
#     response = client.put(f"{URL}/{aid}", json=info)
#     assert response.status_code == 200, f"Unexpected status code: {response.status_code}, response: {response.json()}"
#     result = response.json()
#     print(result)

# def test_delete_account(client):
#     response = client.delete(f"{URL}/{del_aid}")
#     assert response.status_code == 200, f"Unexpected status code: {response.status_code}, response: {response.json()}"
#     result = response.json()
#     print(result)

@pytest.mark.order(2)
def test_add_transaction(client):
    info = {
        "value": -1000,
        "currency": "USD",
        "date": datetime.now().isoformat(),
        "name": "Bankomat",
        "category": "Work"
    }
    res = client.post(f"{URL}/transaction/{aid}", json=info)
    assert res.json() if res.status_code == 200 else {"error": res.text}
    result = res.json()
    print(result)

# def test_delete_accounts(client):
#     response = client.delete(f"{URL}/")
#     assert response.status_code == 200, f"Unexpected status code: {response.status_code}, response: {response.json()}"
#     result = response.json()
#     print(result)

# def test_search_account(client):
#     query = "John"
#     res = client.get(f"{URL}/search/{query}")
#     assert res.json() if res.status_code == 200 else {"error": res.text}
#     result = res.json()
#     print(result)


