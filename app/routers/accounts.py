from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from .. import crud
from app.db.schemas import (
    AccountSchema,
    TransactionSchema
)

router = APIRouter(prefix="/bank", tags=["Accounts"])

@router.post("/")
def create_account_endpoint(account: AccountSchema, db: Session = Depends(get_db)):
    db_account = crud.create_account(db, account)
    # format response (birth_date already stored as datetime)
    return db_account

@router.get("/")
def list_accounts_endpoint(db: Session = Depends(get_db)):
    accounts = crud.get_accounts(db)
    return [a.to_dict() for a in accounts]

@router.get("/search/{aid}")
def get_account_endpoint(aid: str, db: Session = Depends(get_db)):
    acc = crud.get_account(db, aid)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc.to_dict()

@router.delete("/{aid}")
def delete_account_endpoint(aid: str, db: Session = Depends(get_db)):
    return crud.delete_account(db, aid)


@router.delete("/")
def delete_accounts_endpoint(db: Session = Depends(get_db)):
    return crud.delete_accounts(db)
@router.get("/transactions/{aid}")
def get_transactions_endpoint(aid: str, db: Session = Depends(get_db)):
    txs = crud.get_transactions_by_account(db, aid)
    return [t.to_dict() for t in txs]

@router.post("/transaction/{aid}")
def add_transaction_endpoint(aid: str, transaction: TransactionSchema, db: Session = Depends(get_db)):
    tx = crud.create_transaction(aid, db, transaction)
    return tx
