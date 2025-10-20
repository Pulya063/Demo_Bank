from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum as sqlEnum
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.db.database import Base
from app.db.enums import Category

class AccountModel(Base):
    __tablename__ = "accounts"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=True)
    balance = Column(Float, default=0.0)

    transactions = relationship("TransactionModel", back_populates="account", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "balance": self.balance,
            "transactions": [t.to_dict() for t in self.transactions]
        }

class TransactionModel(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    value = Column(Float, default=0.0)
    currency = Column(String, nullable=False)
    date = Column(DateTime, nullable=True)
    name = Column(String, nullable=True)
    category = Column(sqlEnum(Category), nullable=False)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)

    account = relationship("AccountModel", back_populates="transactions")

    def to_dict(self):
        return {
            "id": self.id,
            "value": self.value,
            "currency": self.currency,
            # human format DD-MM-YYYY
            "date": self.date.isoformat() if self.date else None,
            "name": self.name,
            "category": self.category.value if hasattr(self.category, "value") else self.category,
            "account_id": self.account_id
        }
