from pydantic import BaseModel, constr, field_validator
from datetime import datetime, date
from typing import List
from app.db.enums import (
    Currency,
    Category
)

class TransactionSchema(BaseModel):
    value: float
    currency: Currency
    date: datetime
    name: constr(min_length=1, max_length=100)
    category: Category

    class Config:
        orm_model = True

    def trn_show(self):
        return {
            "value": self.value,
            "currency": self.currency,
            "date": self.date.isoformat() if hasattr(self.date, "isoformat") else self.date,
            "name": self.name,
            "category": self.category.value,
        }

class BalanceSchema(BaseModel):
    balance: float
    currency: Currency

    class Config:
        orm_model = True


class AccountSchema(BaseModel):
    name: constr(min_length=1, max_length=50)
    surname: constr(min_length=1, max_length=50)
    birth_date: date
    balance: List[BalanceSchema] = []
    transactions: List[TransactionSchema] = []  # завжди список!

    class Config:
        orm_model = True

    @field_validator("birth_date")
    def valid_date(cls, value):
        if value >= date.today():
            raise ValueError("Birth date must be in the past")
        return value

    def acc_show(self, account_id: str):
        return {
            "account_id": account_id,
            "name": self.name,
            "surname": self.surname,
            "birth_date": self.birth_date.isoformat() if hasattr(self.birth_date, "isoformat") else self.birth_date,
            "balance": self.balance,
            "transactions": [t.trn_show() for t in self.transactions],
        }