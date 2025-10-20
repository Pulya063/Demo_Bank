from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from app.db.models import AccountModel, TransactionModel
from app.db.schemas import AccountSchema, TransactionSchema


def create_account(db: Session, account: AccountSchema) -> AccountModel:
    account_data = account.model_dump()
    # гарантуємо, що transactions завжди список
    if account_data.get('transactions') is None:
        account_data['transactions'] = []

    db_account = AccountModel(**account_data)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def create_transaction(aid: str, db: Session, transaction: TransactionSchema) -> TransactionModel:
    account = get_account(db, aid)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account {aid} not found")

    db_transaction = TransactionModel(
        id=str(uuid4()),
        account_id=account.id,
        value=transaction.value,
        currency=transaction.currency,
        date=transaction.date,
        name=transaction.name,
        category=transaction.category.value
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction.to_dict()


def delete_account(db: Session, aid: str):
    account = get_account(db, aid)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account {aid} not found")
    db.delete(account)
    db.commit()
    return {
        "detail": f"Account {aid} deleted successfully",
        "remaining_accounts": get_accounts(db)
    }

def delete_accounts(db:Session):
    accounts = db.query(AccountModel).all()
    for i in accounts:
        db.delete(i)
    db.commit()
    return {
        "detail": f"All accounts deleted successfully",
        "remaining_accounts": get_accounts(db)
    }

def search_account(db: Session, text: str):
    return db.query(AccountModel).filter(AccountModel.name.ilike(f"%{text}%")).all()


def get_account(db: Session, aid: str):
    return db.query(AccountModel).filter(AccountModel.id == aid).first()


def get_accounts(db: Session):
    return db.query(AccountModel).all()


def get_transactions_by_account(db: Session, aid: str):
    account = get_account(db, aid)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account {aid} not found")
    return db.query(TransactionModel).filter(TransactionModel.account_id == account.id).all()


def get_transactions(db: Session):
    return db.query(TransactionModel).all()
