from typing import Any

from fastapi import APIRouter

from src.stats.schemas import StatsResponse
from src.stats.service import get_transactions_table_stats

router = APIRouter()


@router.get("/stats", response_model=StatsResponse)
async def get_transaction_by_hash() -> dict[str, Any]:
    stats_data = await get_transactions_table_stats()
    print(f"stats_data: {stats_data}")
    return StatsResponse.parse_obj(stats_data)
