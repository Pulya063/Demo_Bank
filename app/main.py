import uvicorn
from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import accounts

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Tracker (SQLite)")

app.include_router(accounts.router)

@app.get("/")
def root():
    return {"message": "API running. See /docs for OpenAPI UI."}


def main():
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)