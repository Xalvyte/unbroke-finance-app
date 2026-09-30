from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4

#Models
class TransactionCreate(BaseModel):
    description: str
    amount: float
    category: str

class TransactionUpdate(BaseModel):
    description: str | None = None
    amount: float | None = None
    category: str | None = None

class Transaction(TransactionCreate):
    id: str = Field(default_factory=lambda: uuid4().hex)

transactions = []

#API

app = FastAPI()

#=================================== GET ===========================================

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"Wave": "This is a refresher program by Rhod."}

@app.get("/transactions")
def get_transactions():
    return transactions

@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str):
    for t in transactions:
        if t.id == transaction_id:
            return t
    raise HTTPException(status_code=404, detail="Transaction not found")

#------------------------ POST --------------------------------------

@app.post("/transactions")
def add_transaction(data: TransactionCreate):
    transaction = Transaction(**data.model_dump())
    transactions.append(transaction)
    return transaction

@app.post("/transactions/{transaction_id}")
def edit_transaction(data):
    print()

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX DELETE XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: str):
    for t in transactions:
        if t.id == transaction_id:
            transactions.remove(t)
            return {"message": "Transaction deleted", "deleted": t}
    raise HTTPException(status_code=404, detail="Transaction does not exist")

#@@@@@@@@@@@@@@@@@@@@@@@@@@@ Patch @@@@@@@@@@@@@@@@@@@@@

@app.patch("/transactions/{transaction_id}")
def patch_transaction(transaction_id: str, data: TransactionUpdate):
    changes = data.model_dump(exclude_unset=True)
    for t in transactions:
        if t.id == transaction_id:
            for field, value in changes.items():
                setattr(t, field, value)
            return t 
    raise HTTPException(status_code=404, detail="Transaction does not exist")
