from databases.interfaces import Record

from src.database import database


async def get_transactions_table_stats() -> Record | None:
    select_query = """
        SELECT 
            COUNT(*) AS total_transactons_in_db,
            SUM(gas_used) AS totl_gas_used,
            SUM(gas_cost_in_usd) AS total_gas_cost_in_dollars
        FROM transaction ps
    """

    return await database.fetch_one(select_query)
