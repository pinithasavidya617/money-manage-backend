import sys
import os
import asyncio
from datetime import date
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

# Add current directory to path
sys.path.append(os.getcwd())

from schemas.transactions import TransactionCreate, TransactionUpdate
from services import transactions as transaction_service

async def test_crud_logic():
    print("Testing CRUD Service Logic (with Mocked Session)...")
    
    # Mock AsyncSession
    mock_session = AsyncMock()
    
    # Test Create
    transaction_data = TransactionCreate(
        title="Test Transaction",
        amount=Decimal("100.00"),
        transaction_type="expense",
        category="Test",
        transaction_date=date.today()
    )
    
    # Mock commit and refresh
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    print("Running create_transaction...")
    try:
        result = await transaction_service.create_transaction(mock_session, transaction_data)
        print(f"[OK] create_transaction logic check passed: {result.title}")
    except Exception as e:
        print(f"[FAIL] create_transaction logic check failed: {e}")

    # Test Get List
    print("Running get_transactions...")
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = []
    mock_session.execute.return_value = mock_result
    
    try:
        results = await transaction_service.get_transactions(mock_session)
        print(f"[OK] get_transactions logic check passed (returned {len(results)} items)")
    except Exception as e:
        print(f"[FAIL] get_transactions logic check failed: {e}")

    print("\nAll logical CRUD checks completed.")

if __name__ == "__main__":
    asyncio.run(test_crud_logic())
