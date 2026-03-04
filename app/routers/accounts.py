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
    """Creates a new bank account."""
    db_account = crud.create_account(db, account)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account haven't been created!")
    return db_account

@router.put("/{aid}")
def update_account(aid:str, account:AccountSchema, db: Session = Depends(get_db)):
    """Updates an existing account."""
    db_account = crud.update_account(db, aid, account)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account haven`t been updated")
    return db_account

@router.get("/{aid}")
def get_account_endpoint(aid: str, db: Session = Depends(get_db)):
    """Retrieves account details by ID."""
    db_account = crud.get_account(db, aid)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@router.get("/")
def list_accounts_endpoint(db: Session = Depends(get_db)):
    """Lists all accounts."""
    accounts = crud.get_accounts(db)
    return [a.to_dict() for a in accounts]

@router.get("/search/{query}")
def search_account(query: str,db: Session = Depends(get_db)):
    """Searches for accounts matching the query."""
    acc = crud.search_account(db, query)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc

@router.delete("/{aid}")
def delete_account_endpoint(aid: str, db: Session = Depends(get_db)):
    """Deletes a specific account."""
    account = crud.get_account(db, aid)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    crud.delete_account(db, aid)
    return {"detail": "deleted successfully"}

@router.get("/currencies")
def get_currencies_endpoint():
    """Returns a list of supported currencies."""
    currencies = [c.value for c in Currency]
    return currencies

@router.get("/category")
def get_categories():
    """Returns a list of transaction categories."""
    categories = [i for i in Category]
    if not categories:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories
@router.delete("/")
def delete_accounts_endpoint(db: Session = Depends(get_db)):
    """Deletes all accounts."""
    accounts = crud.delete_accounts(db)
    if not accounts:
        raise HTTPException(status_code=404, detail="Account haven`t been deleted")
    return accounts

@router.get("/transactions/{aid}")
def get_transactions_endpoint(aid: str, db: Session = Depends(get_db)):
    """Retrieves transactions for a specific account."""
    txs = crud.get_transactions_by_account(db, aid)
    if not txs:
        raise HTTPException(status_code=404, detail="Transactions not found")
    return [t.to_dict() for t in txs]

@router.get("/balance/{aid}")
def balance(aid: str, db: Session = Depends(get_db)):
    """Retrieves the balance of a specific account."""
    bal = crud.get_balance(db, aid)
    if not bal:
        raise HTTPException(status_code=404, detail="Balance not found")
    return bal
@router.post("/transaction/{aid}")
def add_transaction_endpoint(aid: str, transaction: TransactionSchema, db: Session = Depends(get_db)):
    """Adds a new transaction to an account."""
    tx = crud.create_transaction(aid, db, transaction)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx
