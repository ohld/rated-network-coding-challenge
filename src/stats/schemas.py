from decimal import Decimal

from src.models import ORJSONModel


class StatsResponse(ORJSONModel):
    total_transactions_in_db: int
    total_gas_used_gwei: Decimal | None
    total_gas_cost_in_usd: Decimal | None
