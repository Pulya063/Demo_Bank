from datetime import datetime

from app.db.enums import Currency, Category
from conftest import *

URL = "/bank"


class TestTransactions:
    """Transaction tests"""

    def test_add_transaction_success(self, client, sample_account_data, sample_transaction_data):
        """Test successful adding of a transaction"""
        # Create account
        create_response = client.post(f"{URL}/", json=sample_account_data)
        account_id = create_response.json()["id"]

        # Add transaction
        response = client.post(
            f"{URL}/transaction/{account_id}",
            json=sample_transaction_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["value"] == 500.0
        assert data["currency"] == Currency.USD.value
        assert data["category"] == Category.WORK.value
        assert data["account_id"] == account_id

    def test_add_transaction_to_nonexistent_account(self, client, sample_transaction_data):
        """Test adding a transaction to a non-existent account"""
        fake_id = "00000000-0000-0000-0000-000000000000"

        response = client.post(
            f"{URL}/transaction/{fake_id}",
            json=sample_transaction_data
        )

        assert response.status_code == 400

    def test_add_negative_transaction(self, client, sample_account_data):
        """Test adding a negative transaction (expense)"""
        create_response = client.post(f"{URL}/", json=sample_account_data)
        account_id = create_response.json()["id"]

        negative_transaction = {
            "value": -200.0,
            "currency": Currency.USD.value,
            "date": datetime.now().isoformat(),
            "name": "Purchase",
            "category": Category.FOOD.value
        }

        response = client.post(
            f"{URL}/transaction/{account_id}",
            json=negative_transaction
        )

        assert response.status_code == 200

    def test_add_multiple_transactions(self, client, sample_account_data):
        """Test adding multiple transactions"""
        create_response = client.post(f"{URL}/", json=sample_account_data)
        account_id = create_response.json()["id"]

        transactions = [
            {
                "value": 1000.0,
                "currency": Currency.USD.value,
                "date": datetime.now().isoformat(),
                "name": "Salary",
                "category": Category.WORK.value
            },
            {
                "value": -50.0,
                "currency": Currency.USD.value,
                "date": datetime.now().isoformat(),
                "name": "Coffee",
                "category": Category.COFFEE_SNACKS.value
            },
            {
                "value": -200.0,
                "currency": Currency.USD.value,
                "date": datetime.now().isoformat(),
                "name": "Groceries",
                "category": Category.GROCERIES.value
            }
        ]

        for txn in transactions:
            response = client.post(
                f"{URL}/transaction/{account_id}",
                json=txn
            )
            assert response.status_code == 200

    def test_get_transactions_by_account(self, client, sample_account_data, sample_transaction_data):
        """Test retrieving transactions for an account"""
        # Create account
        create_response = client.post(f"{URL}/", json=sample_account_data)
        account_id = create_response.json()["id"]

        # Add transactions
        client.post(f"{URL}/transaction/{account_id}", json=sample_transaction_data)

        second_transaction = sample_transaction_data.copy()
        second_transaction["value"] = -100.0
        second_transaction["category"] = Category.FOOD.value
        client.post(f"{URL}/transaction/{account_id}", json=second_transaction)

        # Retrieve transactions
        response = client.get(f"{URL}/transactions/{account_id}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert isinstance(data, list)

    def test_get_transactions_empty(self, client, sample_account_data):
        """Test retrieving transactions for an account with no transactions"""
        create_response = client.post(f"{URL}/", json=sample_account_data)
        account_id = create_response.json()["id"]

        response = client.get(f"{URL}/transactions/{account_id}")

        assert response.status_code == 404

    def test_get_transactions_nonexistent_account(self, client):
        """Test retrieving transactions for a non-existent account"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"{URL}/transactions/{fake_id}")

        assert response.status_code == 404