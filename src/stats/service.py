from databases.interfaces import Record

from src.database import database


async def get_transactions_table_stats() -> Record | None:
    # I personally prefer raw SQL queries for complex stuff
    # rather than ORM syntax
    select_query = """
        SELECT 
            COUNT(*) AS total_transactions_in_db,
            SUM(gas_used_gwei) AS total_gas_used_gwei,
            SUM(gas_used_usd) AS total_gas_cost_in_usd
        FROM transactions ps
    """

    return await database.fetch_one(select_query)
