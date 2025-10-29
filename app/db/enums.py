from enum import Enum

class Category(str, Enum):
    FOOD = "Food"
    RESTAURANTS = "Restaurants"
    COFFEE_SNACKS = "Coffee & Snacks"
    GROCERIES = "Groceries"
    TAKEAWAY = "Takeaway"

    WORK = "Work"

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

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    UAH = "UAH"
    GBP = "GBP"
    PLN = "PLN"
