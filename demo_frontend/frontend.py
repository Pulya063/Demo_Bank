import streamlit as st
import requests
from datetime import datetime, date

BACKEND_URL = "http://127.0.0.1:8011/bank"

st.set_page_config(page_title="Bank Account Manager", page_icon="💳", layout="centered")

st.title("💳 Bank Account Manager")

# === Функції ===
def get_all_accounts():
    res = requests.get(f"{BACKEND_URL}/")
    return res.json() if res.status_code == 200 else {"error": res.text}

def create_account(name, surname, birth_date, balance):
    info = {
        "name": name,
        "surname": surname,
        "birth_date": birth_date.isoformat(),
        "balance": balance,
        "transactions": []
    }
    res = requests.post(f"{BACKEND_URL}/", json=info)
    return res.json() if res.status_code == 200 else {"error": res.text}

def delete_accounts():
    res = requests.delete(f"{BACKEND_URL}/")
    return res.json() if res.status_code == 200 else {"error": res.text}

def update_account(aid, name, surname, date, balance):
    info = {
        "name": name,
        "surname": surname,
        "birth_date": date.isoformat(),
        "balance": balance,
        "transactions": []
    }

    res = requests.put(f"{BACKEND_URL}/{aid}", json=info)
    return res.json() if res.status_code == 200 else {"error": res.text}


def delete_account(account_id):
    res = requests.delete(f"{BACKEND_URL}/{account_id}")
    return res.json() if res.status_code == 200 else {"error": res.text}

def search_account(query):
    res = requests.get(f"{BACKEND_URL}/search/{query}")
    return res.json() if res.status_code == 200 else {"error": res.text}

def add_transaction(aid, value, currency, date, name, category):
    time_val = st.text_input("Time (HH:MM:SS)", value=datetime.now().strftime("%H:%M:%S"))
    time = datetime.strptime(time_val, "%H:%M:%S").time()
    all_date = datetime.combine(date, time)
    info = {
        "id": "",
        "value": value,
        "currency": currency,
        "date": all_date.isoformat(),
        "name": name,
        "category": category
    }
    res = requests.post(f"{BACKEND_URL}/transaction/{aid}", json=info)
    return res.json() if res.status_code == 200 else {"error": res.text}

def show_transactions(aid):
    res = requests.get(f"{BACKEND_URL}/transactions/{aid}")
    return res.json() if res.status_code == 200 else {"error": res.text}


# === Інтерфейс ===
tabs = st.tabs([
    "📋 All Accounts",
    "➕ Create Account",
    "✏️ Update Account",
    "❌ Delete Account",
    "❌ Delete Accounts",
    "🔍 Search Account",
    "💸 Add Transaction",
    "📜 Show Transactions"
])

# --- Вкладка: всі акаунти ---
with tabs[0]:
    st.subheader("📋 All Accounts")
    if st.button("Refresh Accounts", key="refresh_accounts"):
        data = get_all_accounts()
        st.json(data)

# --- Вкладка: створення ---
with tabs[1]:
    st.subheader("➕ Create Account")
    name = st.text_input("Name", key="create_name")
    surname = st.text_input("Surname", key="create_surname")
    birth_date = st.date_input("Birth Date", value=date(2000, 1, 1), key="create_birth")
    balance = st.number_input("Balance", min_value=0.0, step=0.01, key="create_balance")

    if st.button("Create Account", key="create_btn"):
        result = create_account(name, surname, birth_date, balance)
        st.json(result)

# --- Вкладка: оновлення ---
with tabs[2]:
    st.subheader("✏️ Update Account")
    aid = st.selectbox("Accoun ID", [i["id"] for i in get_all_accounts()], key="update_aid")

    res = requests.get(f"{BACKEND_URL}/account/{aid}")
    account = res.json()
    if account:
        name = st.write(account["name"])
        surname = st.write(account["surname"])
        date_str = account["birth_date"]
        birth_date_obj = datetime.fromisoformat(date_str).date()
        w_date = st.write(birth_date_obj.isoformat())
        balance = st.write(account["balance"])
    else:
        st.warning("Please check the Account ID first")

    u_name = st.text_input("Name", key="update_name")
    u_surname = st.text_input("Surname", key="update_surname")
    u_birth_date = st.date_input("Birth Date", value=date(2000, 1, 1), key="update_birth")
    u_balance = st.number_input("Balance", min_value=0.0, step=0.01, key="update_balance")

    if st.button("Update Account", key="update_account_btn"):
        result = update_account(aid, u_name, u_surname, u_birth_date, u_balance)
        if result == "error":
            st.error("error")
        else:
            st.json(result)
            st.success("success")


with tabs[3]:
    st.subheader("❌ Delete Account")
    del_id = st.selectbox("Account ID", [i["id"] for i in get_all_accounts()], key="delete_id")
    res = requests.get(f"{BACKEND_URL}/account/{del_id}")
    del_account = res.json()

    if del_account:
        name = st.write(del_account["name"])
        surname = st.write(del_account["surname"])
        date_str = del_account["birth_date"]
        birth_date_obj = datetime.fromisoformat(date_str).date()
        w_date = st.write(birth_date_obj.isoformat())
        balance = st.write(del_account["balance"])
    else:
        st.warning("Please check the Account ID first")

    if st.button("Delete Account", key="delete_btn"):
        result = delete_account(del_id)
        st.json(result)

with tabs[4]:
    st.subheader("❌ Delete Accounts")
    if st.button("Delete Accounts", key="delete_all_btn"):
        result = delete_accounts()
        st.json(result)

# --- Вкладка: пошук ---
with tabs[5]:
    st.subheader("🔍 Search Account")
    query = st.text_input("Search query", key="search_query")
    if st.button("Search", key="search_btn"):
        result = search_account(query)
        st.json(result)

# --- Вкладка: додавання транзакції ---
with tabs[6]:
    st.subheader("💸 Add Transaction")
    res = requests.get(f"{BACKEND_URL}/account/{aid}")
    account = res.json

    aid = st.selectbox("Account ID",[i["id"] for i in get_all_accounts()], key="add_aid")
    value = st.number_input("Value", step=0.01, key="tx_value")
    currency = st.selectbox("Currency", ["USD", "EUR", "PLN", "UAH"], key="tx_currency")
    date = st.date_input("Date", value=datetime.now().date(), key="tx_date")
    name_tx = st.text_input("Transaction Name", key="tx_name")

    category = st.selectbox("Category", [
        "Food","Restaurants","Coffee & Snacks","Groceries","Takeaway",
        "Transport","Taxi","Fuel","Public Transport","Car Maintenance",
        "Entertainment","Movies","Music & Streaming","Travel","Hobbies"
    ], key="tx_category")

    if st.button("Add Transaction", key="tx_btn"):
        result = add_transaction(aid, value, currency, date, name_tx, category)
        st.json(result)

# --- Вкладка: перегляд транзакцій ---
with tabs[7]:
    st.subheader("📜 Show Transactions")
    aid_tx = st.selectbox("Account ID",[i["id"] for i in get_all_accounts()],key="id")
    if st.button("Show Transactions", key="show_tx_btn"):
        result = show_transactions(aid_tx)
        st.json(result)
