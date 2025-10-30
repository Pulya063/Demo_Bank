from typing import Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from app.db.models import AccountModel, TransactionModel, BalanceModel
from app.db.schemas import AccountSchema, TransactionSchema, Currency


def create_account(db: Session, account: AccountSchema) -> dict[str, str | None | list[Any] | Any]:
    try:
        account_data = account.model_dump()

        if account_data.get('transactions') is None:
            account_data['transactions'] = []

        db_account = AccountModel(**account_data)

        db.add(db_account)
        db.commit()
        db.refresh(db_account)

        db_balance = BalanceModel(
            id=str(uuid4()),
            currencies={cur.value: 0 for cur in Currency},
            account_id=db_account.id
        )


        db.add(db_balance)
        db.commit()
        return db_account.to_dict()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating account: {e}")


def create_transaction(aid: str, db: Session, transaction: TransactionSchema) -> TransactionModel:
    try:
        transaction_data = transaction.model_dump()
        if transaction_data is None:
            raise HTTPException(status_code=404, detail="Transaction data not found")

        db_transaction = TransactionModel(**transaction_data, account_id=aid)
        db.add(db_transaction)

        account = get_account(db, aid)

        balance_record = db.query(BalanceModel).filter(BalanceModel.account_id == aid).first()
        if not balance_record:
            raise HTTPException(status_code=404, detail="Balance not found")

        cur = db_transaction.currency
        if cur not in balance_record.currencies:
            balance_record.currencies[cur] = 0
        balance_record.currencies[cur] += db_transaction.value

        db.commit()
        db.refresh(db_transaction)
        db.refresh(account)

        return db_transaction
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating transaction: {e}")


def delete_account(db: Session, aid: str):
    account = get_account(db, aid)
    if account:
        db.delete(account)
        db.commit()
        return {
            "detail": f"Account {aid} deleted successfully",
            "remaining_accounts": get_accounts(db)
        }
    raise HTTPException(status_code=404, detail=f"Account {aid} not found")

def delete_accounts(db:Session):
    try:
        accounts = db.query(AccountModel).all()
        for i in accounts:
            db.delete(i)
        db.commit()
        return {
            "detail": "All accounts deleted successfully",
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail="There was an error deleting accounts")

def search_account(db: Session, text: str):
    accounts = db.query(AccountModel).filter(AccountModel.name.ilike(f"%{text}%")).all()
    if not accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return [acc.to_dict() for acc in accounts]


def get_account(db: Session, aid: str):
    return db.query(AccountModel).filter(AccountModel.id == aid).first()

def update_account(db:Session, aid:str, account:AccountSchema):
    try:
        db_account = get_account(db, aid)

        if db_account is None:
            raise HTTPException(status_code=404, detail=f"Account {aid} not found")

        data = account.model_dump(exclude_unset=True)

        for key, value in data.items():
            if value == [] or (isinstance(value, str) and value.strip() == ""):
                continue
            setattr(db_account, key, value)

        db.commit()
        db.refresh(db_account)
        return db_account
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Error updating account: {e}")

def get_balance(db: Session, aid):
    balance =  db.query(BalanceModel).filter(BalanceModel.account_id == aid).first()
    if not balance:
        raise HTTPException(status_code=404, detail=f"Account balance {aid} not found")
    return balance

def get_accounts(db: Session):
    account = db.query(AccountModel).all()
    if not account:
        raise HTTPException(status_code=404, detail=f"Account not found")
    return account

def get_transactions_by_account(db: Session, aid: str):
    account = get_account(db, aid)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account {aid} not found")
    return db.query(TransactionModel).filter(TransactionModel.account_id == aid).all()

def get_transactions(db: Session):
    return db.query(TransactionModel).all()
