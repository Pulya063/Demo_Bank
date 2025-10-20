from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from enum import Enum
from typing import List, Optional


class Category(str, Enum):
    FOOD = "Food"
    RESTAURANTS = "Restaurants"
    COFFEE_SNACKS = "Coffee & Snacks"
    GROCERIES = "Groceries"
    TAKEAWAY = "Takeaway"
    TRANSPORT = "Transport"
    TAXI = "Taxi"
    FUEL = "Fuel"
    PUBLIC_TRANSPORT = "Public Transport"
    CAR_MAINTENANCE = "Car Maintenance"
    RENT = "Rent"
    UTILITIES = "Utilities"
    INTERNET_PHONE = "Internet & Phone"
    REPAIRS = "Repairs"
    ENTERTAINMENT = "Entertainment"
    MOVIES = "Movies"
    MUSIC_STREAMING = "Music & Streaming"
    TRAVEL = "Travel"
    HOBBIES = "Hobbies"
    CLOTHING = "Clothing"
    SHOES = "Shoes"
    ACCESSORIES = "Accessories"
    HEALTH = "Health"
    PHARMACY = "Pharmacy"
    FITNESS_SPORTS = "Fitness & Sports"
    BEAUTY_SPA = "Beauty & Spa"
    EDUCATION = "Education"
    BOOKS_SUPPLIES = "Books & Supplies"
    COURSES_TRAINING = "Courses & Training"
    BANKING_FEES = "Banking Fees"
    INVESTMENTS = "Investments"
    INSURANCE = "Insurance"
    TAXES = "Taxes"
    GIFTS_DONATIONS = "Gifts & Donations"
    PERSONAL_CARE = "Personal Care"
    MISCELLANEOUS = "Miscellaneous"


class TransactionSchema(BaseModel):
    value: float
    currency: str
    date: datetime
    name: str
    category: Category

    @field_validator('date')
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Date must be in format DD-MM-YYYY")
        return value

    def trn_show(self):
        return {
            "value": self.value,
            "currency": self.currency,
            "date": self.date.isoformat() if hasattr(self.date, "isoformat") else self.date,
            "name": self.name,
            "category": self.category.value,
        }


class AccountSchema(BaseModel):
    name: str
    surname: str
    birth_date: datetime
    balance: float = 0.0
    transactions: List[TransactionSchema] = []  # завжди список!

    @field_validator('birth_date')
    def parse_birth_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Birth date must be in format DD-MM-YYYY")
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
