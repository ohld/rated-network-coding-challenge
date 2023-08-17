from typing import Any
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, validator, root_validator

from src.models import ORJSONModel


class TransactionCompactResponse(ORJSONModel):
    hash: str
    from_address: str
    to_address: str
    block_number: int
    block_timestamp: datetime
    gas_used_gwei: Decimal | None
    gas_used_usd: Decimal | None


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
    receipts_contract_address: str | None
    receipts_root: str | None
    receipts_status: bool
    receipts_effective_gas_price: float
    gas_used_gwei: float | None


    @validator("block_timestamp", pre=True)
    def parse_block_timestamp(cls, value: str) -> datetime:
        input_datetime_format = '%Y-%m-%d %H:%M:%S.%f %Z'
        return datetime.strptime(value, input_datetime_format)
    

    @root_validator(skip_on_failure=True)
    def set_tx_url(cls, data: dict[str, Any]) -> dict[str, Any]:
        data["gas_used_gwei"] =  data["receipts_gas_used"] * data["gas_price"] / 10**9
        return data

