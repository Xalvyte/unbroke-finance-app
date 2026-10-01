from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from database import get_db
from models import TransactionDB
from sqlalchemy.orm import Session

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
    model_config = ConfigDict(from_attributes=True)
    id: str

#API

app = FastAPI()

#=================================== GET ===========================================

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"Wave": "This is a refresher program by Rhod."}

@app.get("/transactions", response_model=list[Transaction])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(TransactionDB).all()

@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    row = db.get(TransactionDB, transaction_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return row

#------------------------ POST --------------------------------------

@app.post("/transactions", response_model=Transaction)
def add_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    row = TransactionDB(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX DELETE XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: str, db: Session = Depends(get_db)):
    row = db.get(TransactionDB, transaction_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Transaction does not exist")
    db.delete(row)
    db.commit()
    return {"message": "Transaction deleted", "id": transaction_id}

#@@@@@@@@@@@@@@@@@@@@@@@@@@@ Patch @@@@@@@@@@@@@@@@@@@@@

@app.patch("/transactions/{transaction_id}", response_model=Transaction)
def patch_transaction(transaction_id: str, data: TransactionUpdate, db: Session = Depends(get_db)):
    row = db.get(TransactionDB, transaction_id)

    if row is None:
        raise HTTPException(status_code=404, detail="Transaction does not exist")

    changes = data.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in changes.items():
        setattr(row, field, value)

    db.commit()
    db.refresh(row)
    return row


