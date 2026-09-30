from uuid import uuid4
from sqlalchemy import String, Float 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TransactionDB(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: uuid4().hex)
    description: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String)