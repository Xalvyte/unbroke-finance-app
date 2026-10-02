from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from database import get_db
from models import TransactionDB, UserDB
from sqlalchemy.orm import Session
from security import hash_password

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

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: str

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

@app.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(UserDB).filter(UserDB.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = UserDB(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

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


