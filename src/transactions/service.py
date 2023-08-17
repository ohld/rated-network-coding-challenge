import logging
from datetime import datetime

from databases.interfaces import Record
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from src.database import database, transactions
from src.transactions.prices import get_eth_price

logger = logging.getLogger(__name__)


# TODO: query only compact data?
async def get_transaction_by_hash(tx_hash: str) -> Record | None:
    select_query = select(transactions).where(transactions.c.hash == tx_hash)
    return await database.fetch_one(select_query)


async def insert_transaction_data(transaction_data):
    insert_query = (
        insert(transactions)
        .values(
            hash=transaction_data.hash,
            nonce=transaction_data.nonce,
            block_hash=transaction_data.block_hash,
            block_number=transaction_data.block_number,
            transaction_index=transaction_data.transaction_index,
            from_address=transaction_data.from_address,
            to_address=transaction_data.to_address,
            value=transaction_data.value,
            gas=transaction_data.gas,
            gas_price=transaction_data.gas_price,
            block_timestamp=transaction_data.block_timestamp,
            max_fee_per_gas=transaction_data.max_fee_per_gas,
            max_priority_fee_per_gas=transaction_data.max_priority_fee_per_gas,
            transaction_type=transaction_data.transaction_type,
            receipts_cumulative_gas_used=transaction_data.receipts_cumulative_gas_used,
            receipts_gas_used=transaction_data.receipts_gas_used,
            receipts_contract_address=transaction_data.receipts_contract_address,
            receipts_root=transaction_data.receipts_root,
            receipts_status=transaction_data.receipts_status,
            receipts_effective_gas_price=transaction_data.receipts_effective_gas_price,
            gas_used_gwei=transaction_data.gas_used_gwei,
        )
        .on_conflict_do_nothing()  # TODO: specify constraint
    )

    await database.fetch_one(insert_query)


async def set_transaction_usd_price(tx_hash: str, gas_used_usd: float) -> None:
    update_query = (
        update(transactions)
        .values({"gas_used_usd": gas_used_usd})
        .where(transactions.c.hash == tx_hash)
    )

    await database.execute(update_query)


async def calculate_transaction_gas_used_usd(
    tx_hash: str, block_timestamp: datetime, gas_used_gwei: float
) -> None:
    eth_price = await get_eth_price(block_timestamp)
    if eth_price is None:
        logger.warning(
            f"Failed to query eth_price for block_timestamp: {block_timestamp}"
        )
        return

    gas_used_usd = eth_price * gas_used_gwei / 10**9

    await set_transaction_usd_price(tx_hash, gas_used_usd)
