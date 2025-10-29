from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app import crud
from app.db.enums import Category, Currency
from app.db.schemas import (
    AccountSchema,
    TransactionSchema
)

router = APIRouter(prefix="/bank", tags=["Accounts"])

@router.post("/")
def create_account_endpoint(account: AccountSchema, db: Session = Depends(get_db)):
    db_account = crud.create_account(db, account)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account haven't been created!")
    return db_account

@router.put("/{aid}")
def update_account(aid:str, account:AccountSchema, db: Session = Depends(get_db)):
    db_account = crud.update_account(db, aid, account)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account haven`t been updated")
    return db_account

@router.get("/account/{aid}")
def get_account_endpoint(aid: str, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, aid)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@router.get("/")
def list_accounts_endpoint(db: Session = Depends(get_db)):
    accounts = crud.get_accounts(db)
    return [a.to_dict() for a in accounts]

@router.get("/search/{query}")
def search_account(query: str,db: Session = Depends(get_db)):
    acc = crud.search_account(db, query)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc

@router.delete("/{aid}")
def delete_account_endpoint(aid: str, db: Session = Depends(get_db)):
    account =  crud.delete_account(db, aid)
    if not account:
        raise HTTPException(status_code=404, detail="Account haven`t been deleted")

@router.get("/currencies")
def get_currencies_endpoint():
    currencies = [i for i in Currency]
    if not currencies:
        raise HTTPException(status_code=404, detail="Currencies not found")
    return currencies

@router.get("/category")
def get_categories():
    categories = [i for i in Category]
    if not categories:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories
@router.delete("/")
def delete_accounts_endpoint(db: Session = Depends(get_db)):
    accounts = crud.delete_accounts(db)
    if not accounts:
        raise HTTPException(status_code=404, detail="Account haven`t been deleted")
    return accounts

@router.get("/transactions/{aid}")
def get_transactions_endpoint(aid: str, db: Session = Depends(get_db)):
    txs = crud.get_transactions_by_account(db, aid)
    if not txs:
        raise HTTPException(status_code=404, detail="Transactions not found")
    return [t.to_dict() for t in txs]

@router.get("/balance/{aid}")
def balance(aid: str, db: Session = Depends(get_db)):
    bal = crud.get_balance(db, aid)
    if not bal:
        raise HTTPException(status_code=404, detail="Balance not found")
    return bal
@router.post("/transaction/{aid}")
def add_transaction_endpoint(aid: str, transaction: TransactionSchema, db: Session = Depends(get_db)):
    tx = crud.create_transaction(aid, db, transaction)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx
