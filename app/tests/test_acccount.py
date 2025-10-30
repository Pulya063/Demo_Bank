from datetime import date
from conftest import *

URL = "/bank"


class TestAccountCRUD:

    def test_create_account_success(self, client, sample_account_data):
        response = client.post(f"{URL}/", json=sample_account_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Ivan"
        assert data["surname"] == "Petrenko"
        assert "id" in data
        assert data["birth_date"] == "2000-01-15"
        assert isinstance(data["transactions"], list)

    def test_create_account_invalid_birth_date(self, client):
        """Test creating an account with a future birth date"""
        future_date = date.today().isoformat()
        invalid_data = {
            "name": "Maria",
            "surname": "Koval",
            "birth_date": future_date,
            "transactions": []
        }

        response = client.post(f"{URL}/", json=invalid_data)
        assert response.status_code == 422  # Validation error

    def test_create_account_missing_required_fields(self, client):
        """Test creating an account missing required fields"""
        incomplete_data = {
            "name": "Test"
            # Missing surname and birth_date
        }

        response = client.post(f"{URL}/", json=incomplete_data)
        assert response.status_code == 422

    def test_create_account_empty_name(self, client):
        """Test creating an account with an empty name"""
        invalid_data = {
            "name": "",
            "surname": "Tester",
            "birth_date": "2000-01-01",
            "transactions": []
        }

        response = client.post(f"{URL}/", json=invalid_data)
        assert response.status_code == 422

    def test_get_account_success(self, client, sample_account_data):
        """Test retrieving an account by ID"""
        # First create an account
        create_response = client.post(f"{URL}/", json=sample_account_data)
        account_id = create_response.json()["id"]

        # Retrieve the account using the base URL variable
        response = client.get(f"{URL}/{account_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == account_id
        assert data["name"] == "Ivan"
        assert data["surname"] == "Petrenko"

    def test_get_account_not_found(self, client):
        """Test retrieving a non-existent account"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"{URL}/{fake_id}")

        assert response.status_code == 404

    def test_list_all_accounts(self, client, sample_account_data):
        """Test listing all accounts"""
        # Create a couple of accounts
        client.post(f"{URL}/", json=sample_account_data)

        second_account = sample_account_data.copy()
        second_account["name"] = "Maria"
        second_account["surname"] = "Koval"
        client.post(f"{URL}/", json=second_account)

        # Get the list
        response = client.get(f"{URL}/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        assert isinstance(data, list)

    def test_list_accounts_empty(self, client):
        """Test listing accounts when the DB is empty"""
        response = client.get(f"{URL}/")

        assert response.status_code == 404

    def test_update_account_success(self, client, sample_account_data):
        """Test successful account update"""
        # Create an account
        create_response = client.post(f"{URL}/", json=sample_account_data)
        account_id = create_response.json()["id"]

        # Update data
        updated_data = {
            "name": "Oleksandr",
            "surname": "Shevchenko",
            "birth_date": "1995-05-20",
            "balance": [],
            "transactions": []
        }

        response = client.put(f"{URL}/{account_id}", json=updated_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Oleksandr"
        assert data["surname"] == "Shevchenko"

    def test_update_account_not_found(self, client):
        """Test updating a non-existent account"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        update_data = {
            "name": "Test",
            "surname": "Tester",
            "birth_date": "2000-01-01",
            "balance": [],
            "transactions": []
        }

        response = client.put(f"{URL}/{fake_id}", json=update_data)

        assert response.status_code == 404

    def test_update_account_partial(self, client, sample_account_data):
        """Test partial account update"""
        create_response = client.post(f"{URL}/", json=sample_account_data)
        account_id = create_response.json()["id"]

        # Update only the name
        partial_update = {
            "name": "NewName",
            "surname": "Petrenko",
            "birth_date": "2000-01-15",
            "balance": [],
            "transactions": []
        }

        response = client.put(f"{URL}/{account_id}", json=partial_update)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "NewName"
        assert data["surname"] == "Petrenko"

    def test_delete_account_success(self, client, sample_account_data):
        """Test successful account deletion"""
        create_response = client.post(f"{URL}/", json=sample_account_data)
        account_id = create_response.json()["id"]

        response = client.delete(f"{URL}/{account_id}")

        assert response.status_code == 200

        # Verify the account no longer exists
        get_response = client.get(f"{URL}/{account_id}")
        assert get_response.status_code == 404

    def test_delete_account_not_found(self, client):
        """Test deleting a non-existent account"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.delete(f"{URL}/{fake_id}")

        assert response.status_code == 404

    def test_delete_all_accounts(self, client, sample_account_data):
        """Test deleting all accounts"""
        # Create a couple of accounts
        client.post(f"{URL}/", json=sample_account_data)
        second_account = sample_account_data.copy()
        second_account["name"] = "Maria"
        client.post(f"{URL}/", json=second_account)

        response = client.delete(f"{URL}/")

        assert response.status_code == 200
        assert "deleted successfully" in response.json()["detail"]

    def test_search_account_by_name(self, client, sample_account_data):
        """Test searching accounts by name"""
        client.post(f"{URL}/", json=sample_account_data)

        response = client.get(f"{URL}/search/Ivan")

        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["name"] == "Ivan"

    def test_search_account_not_found(self, client):
        """Test searching for a non-existent account"""
        response = client.get(f"{URL}/search/DoesNotExistAccount")

        assert response.status_code == 404

    def test_search_account_partial_match(self, client, sample_account_data):
        """Test searching with a partial match"""
        client.post(f"{URL}/", json=sample_account_data)

        response = client.get(f"{URL}/search/Iva")

        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0