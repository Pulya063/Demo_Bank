from datetime import datetime
from conftest import *
from app.db.enums import Currency, Category

URL = "/bank"


class TestBalance:
    """Balance tests"""

    def test_get_balance_after_creation(self, client, sample_account_data):
        """Test getting balance after account creation"""
        create_response = client.post(f"{URL}/", json=sample_account_data)
        account_id = create_response.json()["id"]

        response = client.get(f"{URL}/balance/{account_id}")

        assert response.status_code == 200
        data = response.json()
        assert "currencies" in data
        # Balance should be 0 for all currencies
        for currency in Currency:
            assert data["currencies"][currency.value] == 0

    def test_get_balance_not_found(self, client):
        """Test getting balance for a non-existent account"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"{URL}/balance/{fake_id}")

        assert response.status_code == 404

    def test_balance_updates_after_transaction(self, client, sample_account_data):
        """Test balance updates after a transaction"""
        create_response = client.post(f"{URL}/", json=sample_account_data)
        account_id = create_response.json()["id"]

        # Add a transaction
        transaction = {
            "value": 1000.0,
            "currency": Currency.USD.value,
            "date": datetime.now().isoformat(),
            "name": "Deposit",
            "category": Category.WORK.value
        }
        client.post(f"{URL}/transaction/{account_id}", json=transaction)

        # Check balance
        response = client.get(f"{URL}/balance/{account_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["currencies"]["USD"] == 1000.0

    def test_balance_multiple_currencies(self, client, sample_account_data):
        """Test balance with multiple currencies"""
        create_response = client.post(f"{URL}/", json=sample_account_data)
        account_id = create_response.json()["id"]

        # Add transactions in different currencies
        usd_transaction = {
            "value": 500.0,
            "currency": Currency.USD.value,
            "date": datetime.now().isoformat(),
            "name": "USD Deposit",
            "category": Category.WORK.value
        }
        client.post(f"{URL}/transaction/{account_id}", json=usd_transaction)

        eur_transaction = {
            "value": 300.0,
            "currency": Currency.EUR.value,
            "date": datetime.now().isoformat(),
            "name": "EUR Deposit",
            "category": Category.WORK.value
        }
        client.post(f"{URL}/transaction/{account_id}", json=eur_transaction)

        # Check balance
        response = client.get(f"{URL}/balance/{account_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["currencies"]["USD"] == 500.0
        assert data["currencies"]["EUR"] == 300.0


class TestEnums:
    """Tests for enum endpoints"""

    def test_get_currencies(self, client):
        """Test retrieving list of currencies"""
        response = client.get(f"{URL}/currencies")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "USD" in data or Currency.USD in data

    def test_get_categories(self, client):
        """Test retrieving list of categories"""
        response = client.get(f"{URL}/category")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
