from time import strftime

import streamlit as st
import requests
from datetime import datetime, date

BACKEND_URL = "http://127.0.0.1:8006/bank"

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

# def update_account(account_id, name, surname, birth_date, balance):
#     info = {
#         "name": name,
#         "surname": surname,
#         "birth_date": birth_date.strftime("%d-%m-%Y"),
#         "balance": balance,
#         "transactions": None
#     }
#     res = requests.put(f"{BACKEND_URL}/{account_id}", json=info)
#     return res.json() if res.status_code == 200 else {"error": res.text}

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
# with tabs[2]:
#     st.subheader("✏️ Update Account")
#     account_id = st.text_input("Account ID", key="update_id")
#     name_upd = st.text_input("New Name", key="update_name")
#     surname_upd = st.text_input("New Surname", key="update_surname")
#     birth_upd = st.date_input("New Birth Date", value=date(2000, 1, 1), key="update_birth")
#     balance_upd = st.number_input("New Balance", min_value=0.0, step=0.01, key="update_balance")
#
#     if st.button("Update Account", key="update_btn"):
#         result = update_account(account_id, name_upd, surname_upd, birth_upd, balance_upd)
#         st.json(result)

# --- Вкладка: видалення ---
with tabs[3]:
    st.subheader("❌ Delete Account")
    del_id = st.text_input("Account ID", key="delete_id")
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
    aid = st.text_input("Account ID", key="tx_id")
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
    aid_tx = st.text_input("Account ID", key="show_tx_id")
    if st.button("Show Transactions", key="show_tx_btn"):
        result = show_transactions(aid_tx)
        st.json(result)
