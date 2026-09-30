from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import uuid4

#Models
class TransactionCreate(BaseModel):
    
    description: str
    amount: float
    category: str
class Transaction(TransactionCreate):
    id: str = Field(default_factory=lambda: uuid4().hex)

transactions = []

#API

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"Wave": "This is a refresher program by Rhod."}

@app.get("/transactions")
def get_transactions():
    return transactions

@app.post("/transactions")
def add_transactions(data: TransactionCreate):
    transaction = Transaction(**data.model_dump())
    transactions.append(transaction)
    return transaction