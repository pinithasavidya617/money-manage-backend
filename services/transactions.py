from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.transactions import Transaction
from schemas.transactions import TransactionCreate, TransactionUpdate

async def create_transaction(
    session: AsyncSession,
    transaction: TransactionCreate,
) -> Transaction:
    db_transaction = Transaction(
        title=transaction.title,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        category=transaction.category,
        note=transaction.note,
        transaction_date=transaction.transaction_date,
    )

    session.add(db_transaction)

    try:
        await session.commit()
        await session.refresh(db_transaction)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig),
        )

    return db_transaction

async def get_transactions(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[Transaction]:
    query = select(Transaction).offset(skip).limit(limit).order_by(Transaction.transaction_date.desc())
    result = await session.execute(query)
    return list(result.scalars().all())

async def get_transaction(
    session: AsyncSession,
    transaction_id: int,
) -> Optional[Transaction]:
    query = select(Transaction).where(Transaction.id == transaction_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def update_transaction(
    session: AsyncSession,
    transaction_id: int,
    transaction_update: TransactionUpdate,
) -> Optional[Transaction]:
    db_transaction = await get_transaction(session, transaction_id)
    if not db_transaction:
        return None

    update_data = transaction_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)

    try:
        await session.commit()
        await session.refresh(db_transaction)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig),
        )

    return db_transaction

async def delete_transaction(
    session: AsyncSession,
    transaction_id: int,
) -> bool:
    db_transaction = await get_transaction(session, transaction_id)
    if not db_transaction:
        return False

    await session.delete(db_transaction)
    await session.commit()
    return True
