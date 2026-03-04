import uvicorn
from fastapi import FastAPI
from app.db.database import engine, Base, SessionLocal
from app.routers import accounts

# Create database tables based on models
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="Financial Tracker (SQLite)")

# Include routers
app.include_router(accounts.router)

@app.get("/")
def root():
    """Root endpoint to check if API is running."""
    return {"message": "API running. See /docs for OpenAPI UI."}

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8008, reload=True)