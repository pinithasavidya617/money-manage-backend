from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator, ConfigDict

class TransactionBase(BaseModel):
    title: str = Field(..., max_length=255)
    amount: Decimal = Field(..., decimal_places=2)
    transaction_type: Literal["income", "expense"]
    category: Optional[str] = Field(None, max_length=100)
    note: Optional[str] = None
    transaction_date: date

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Amount must be greater than or equal to 0")
        return v

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    amount: Optional[Decimal] = Field(None, decimal_places=2)
    transaction_type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = Field(None, max_length=100)
    note: Optional[str] = None
    transaction_date: Optional[date] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v is not None and v < 0:
            raise ValueError("Amount must be greater than or equal to 0")
        return v

class TransactionRead(TransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True