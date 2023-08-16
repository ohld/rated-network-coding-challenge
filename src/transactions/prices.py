import httpx
import logging

logger = logging.getLogger(__name__)

# async def _get_cached_token_price(chain_id: int, token_address: str) -> dict[str, dict[str, dict[str, float]]] | None:
#     token_price = await redis.get_by_key(redis.get_token_price_key(chain_id, token_address))
#     if not token_price:
#         return None

#     return {str(chain_id): {token_address: {"USD": float(token_price)}}}


async def request_eth_price(unix_timestamp) -> dict[str, dict[str, dict[str, float]]]:
    logger.info(f"Requesting eth price from Coingecko for {unix_timestamp}")

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            "https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range",
            params={
                "vs_currency": "usd",
                "from": unix_timestamp,
                "to": unix_timestamp + 3600,
            },
        )
        resp.raise_for_status()

    eth_price = resp.json()["prices"][0][1]
    logger.info(f"Received eth price for {unix_timestamp}: ${eth_price}")
    return eth_price


# timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
# unix_timestamp = int(timestamp.timestamp())
