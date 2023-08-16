from typing import Any

from fastapi import APIRouter

from src.stats.schemas import StatsResponse
from src.stats.service import get_transactions_table_stats

router = APIRouter()


@router.get("/stats", response_model=StatsResponse)
async def get_transaction_by_hash() -> dict[str, Any]:
    stats_data = await get_transactions_table_stats()
    return stats_data

    # return {
    #     "totalTransactionsInDB": total_transactions,
    #     "totalGasUsed": total_gas_used,
    #     "totalGasCostInDollars": total_gas_cost_in_dollars
    # }
