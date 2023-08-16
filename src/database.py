from databases import Database
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Identity,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    create_engine,
)

from src.config import settings
from src.constants import DB_NAMING_CONVENTION

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

database = Database(DATABASE_URL, force_rollback=settings.ENVIRONMENT.is_testing)


transactions = Table(
    "transactions",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("hash", String, index=True, unique=True),
    Column("nonce", Integer),
    Column("block_hash", String, index=True),
    Column("block_number", Integer),
    Column("transaction_index", Integer),
    Column("from_address", String),
    Column("to_address", String),
    Column("value", Numeric),
    Column("gas", BigInteger),
    Column("gas_price", Numeric),
    Column("block_timestamp", DateTime),
    Column("max_fee_per_gas", Numeric),
    Column("max_priority_fee_per_gas", Numeric),
    Column("transaction_type", String),
    Column("receipts_cumulative_gas_used", BigInteger),
    Column("receipts_gas_used", BigInteger),
    Column("receipts_contract_address", String, nullable=True),
    Column("receipts_root", String, nullable=True),
    Column("receipts_status", Boolean),
    Column("receipts_effective_gas_price", Numeric),
    Column("gas_used_gwei", Numeric),
    Column("gas_used_usd", Numeric),
)

