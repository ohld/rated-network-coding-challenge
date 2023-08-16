from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from src.models import ORJSONModel


class TransactionCompactResponse(ORJSONModel):
    hash: str
    from_address: str
    to_address: str
    block_number: int
    executed_at: datetime
    gas_used: int
    gas_cost_in_dollars: Decimal


class TransactionInsert(BaseModel):
    hash: str
    nonce: int
    block_hash: str
    block_number: int
    transaction_index: int
    from_address: str
    to_address: str
    value: float
    gas: int
    gas_price: int
    block_timestamp: datetime
    max_fee_per_gas: float
    max_priority_fee_per_gas: float
    transaction_type: str
    receipts_cumulative_gas_used: int
    receipts_gas_used: int
    receipts_contract_address: str = None
    receipts_root: str = None
    receipts_status: bool
    receipts_effective_gas_price: float
