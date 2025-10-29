import streamlit as st
import requests
from datetime import datetime, date

BACKEND_URL = "http://127.0.0.1:8007/bank"

st.set_page_config(page_title="Bank Account Manager", page_icon="💳", layout="centered")

st.title("💳 Bank Account Manager")

def get_all_accounts():
    res = requests.get(f"{BACKEND_URL}/")
    return res.json() if res.status_code == 200 else {"error": res.text}

def create_account(name, surname, birth_date):
    info = {
        "name": name,
        "surname": surname,
        "birth_date": birth_date.isoformat(),
        "transactions": []
    }
    res = requests.post(f"{BACKEND_URL}/", json=info)
    return res.json() if res.status_code == 200 else {"error": res.text}

def delete_accounts():
    res = requests.delete(f"{BACKEND_URL}/")
    return res.json() if res.status_code == 200 else {"error": res.text}

def update_account(aid, name, surname, date):
    info = {
        "name": name,
        "surname": surname,
        "birth_date": date.isoformat(),
        "balance": [],
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

def add_transaction(aid, value, currency, name, category):
    info = {
        "id": "",
        "value": value,
        "currency": currency,
        "date": datetime.now().isoformat(),
        "name": name,
        "category": category
    }
    res = requests.post(f"{BACKEND_URL}/transaction/{aid}", json=info)
    return res.json() if res.status_code == 200 else {"error": res.text}

def show_transactions(aid):
    res = requests.get(f"{BACKEND_URL}/transactions/{aid}")
    return res.json() if res.status_code == 200 else {"error": res.text}


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

with tabs[0]:
    st.subheader("📋 All Accounts")
    if st.button("Refresh Accounts", key="refresh_accounts"):
        data = get_all_accounts()
        st.json(data)

with tabs[1]:
    st.subheader("➕ Create Account")
    name = st.text_input("Name", key="create_name")
    surname = st.text_input("Surname", key="create_surname")
    birth_date = st.date_input("Birth Date", value=date(2000, 1, 1), key="create_birth")


    if st.button("Create Account", key="create_btn"):
        result = create_account(name, surname, birth_date)
        st.json(result)

with tabs[2]:
    st.subheader("✏️ Update Account")
    accounts = get_all_accounts() or []
    account_ids = [i.get('id') for i in accounts if 'id' in i]
    aid = st.selectbox("Account ID", account_ids, key="update_aid")

    if aid:
        res = requests.get(f"{BACKEND_URL}/account/{aid}")
        if res.status_code == 200:
            account = res.json()
            st.write(account["name"])
            st.write(account["surname"])
            date_str = account["birth_date"]
            birth_date_obj = date.fromisoformat(date_str)
            st.write(birth_date_obj)
            res = requests.get(f"{BACKEND_URL}/balance/{aid}")
            if res.status_code == 200:
                data = res.json()
                st.write(f"💰 Balance: {data.get('currencies', {})}")
            else:
                st.warning("⚠️ Can't load balance")

            u_name = st.text_input("Name", key="update_name")
            u_surname = st.text_input("Surname", key="update_surname")
            u_birth_date = st.date_input("Birth Date", value=date(2000, 1, 1), key="update_birth")

            if st.button("Update Account", key="update_account_btn"):
                if u_name == "" or u_surname == "" or not isinstance(u_name, str) or isinstance(u_surname, str):
                    st.warning("Please write correct personal information")
                result = update_account(aid, u_name, u_surname, u_birth_date)
                if result.status_code == 200:
                    st.warning(f"Error updating account, statud_code - {result.status_code}")
                else:
                    st.json(result)
                    st.success("Success")
        else:
            st.warning("Please check the Account ID first")
    else:
        st.warning("Please check the Account ID first")


with tabs[3]:
    st.subheader("❌ Delete Account")
    del_id = st.selectbox("Account ID", [i['id'] for i in get_all_accounts()], key="delete_id")
    res = requests.get(f"{BACKEND_URL}/account/{del_id}")
    del_account = res.json()

    if res.status_code == 200:
        name = st.write(del_account["name"])
        surname = st.write(del_account["surname"])
        date_str = del_account["birth_date"]
        birth_date_obj = date.fromisoformat(date_str)
        w_date = st.write(birth_date_obj)
        data = requests.get(f"{BACKEND_URL}/balance/{del_id}")
        del_data = data.json()
        balance = st.write(del_data["currencies"])
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

with tabs[5]:
    st.subheader("🔍 Search Account")
    query = st.text_input("Search query", key="search_query")
    if isinstance(query.strip(), str) or query.strip() == "":
        if st.button("Search", key="search_btn"):
            result = search_account(query)
            st.json(result)

with tabs[6]:
    st.subheader("💸 Add Transaction")
    res = requests.get(f"{BACKEND_URL}/account/{aid}")
    account = res.json()
    if res.status_code == 200:
        name = st.write(account["name"])
        surname = st.write(account["surname"])
        date_str = del_account["birth_date"]
        birth_date_obj = date.fromisoformat(date_str)
        w_date = st.write(birth_date_obj)
        data_txt = requests.get(f"{BACKEND_URL}/balance/{del_id}")
        balance = st.write(data_txt.json())


        aid = st.selectbox("Account ID", [i['id'] for i in get_all_accounts() if i.status_code != 200], key="add_aid")
        value = st.number_input("Value", step=0.01, key="tx_value")
        res = requests.get(f"{BACKEND_URL}/currencies")
        currencies = res.json()
        cat_res = requests.get(f"{BACKEND_URL}/categories")
        categories = cat_res.json()
        currency = st.selectbox("Currency", currencies, key="tx_currency")
        category = st.selectbox("Category", categories, key="tx_category")
        name_tx = st.text_input("Transaction Name", key="tx_name")
    else:
        st.warning("Please check the Account ID first")

    if st.button("Add Transaction", key="tx_btn"):
        result = add_transaction(aid, value, currency, name_tx, category)
        st.json(result)

with tabs[7]:
    st.subheader("📜 Show Transactions")
    aid_tx = st.selectbox("Account ID",[i['id'] for i in get_all_accounts()],key="id")
    if st.button("Show Transactions", key="show_tx_btn"):
        result = show_transactions(aid_tx)
        st.json(result)
