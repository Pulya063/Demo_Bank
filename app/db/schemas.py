from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List
from app.db.enums import (
    Currency,
    Category
)

class TransactionSchema(BaseModel):
    value: float
    currency: Currency
    date: datetime
    name: str
    category: Category

    @field_validator('date')
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Date must be in format DD-MM-YYYY")
        return value


    class Config:
        orm_model = True

    # def trn_show(self):
    #     return {
    #         "value": self.value,
    #         "currency": self.currency,
    #         "date": self.date.isoformat() if hasattr(self.date, "isoformat") else self.date,
    #         "name": self.name,
    #         "category": self.category.value,
    #     }

class BalanceSchema(BaseModel):
    balance: float
    currency: Currency

    class Config:
        orm_model = True


class AccountSchema(BaseModel):
    name: str
    surname: str
    birth_date: datetime
    balance: List[BalanceSchema] = []
    transactions: List[TransactionSchema] = []  # завжди список!

    @field_validator('birth_date')
    def parse_birth_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Birth date must be in format DD-MM-YYYY")
        return value


    class Config:
        orm_model = True

    # def acc_show(self, account_id: str):
    #     return {
    #         "account_id": account_id,
    #         "name": self.name,
    #         "surname": self.surname,
    #         "birth_date": self.birth_date.isoformat() if hasattr(self.birth_date, "isoformat") else self.birth_date,
    #         "balance": self.balance,
    #         "transactions": [t.trn_show() for t in self.transactions],
    #     }
