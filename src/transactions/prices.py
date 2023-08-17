import httpx
import asyncio
import logging
from datetime import datetime

from src import redis
from src.redis import RedisData

logger = logging.getLogger(__name__)


async def _get_cached_eth_price(unix_ts: int) -> float | None:
    token_price = await redis.get_by_key(redis.get_eth_price_key(unix_ts))
    if not token_price:
        return None

    return float(token_price)


async def get_eth_price(block_datetime: datetime) -> float:
    unix_ts = int(block_datetime.timestamp()) // 3600 * 3600  # TODO: lambda unix_ts_rounded_hourly

    eth_price = await _get_cached_eth_price(unix_ts)
    if not eth_price:
        eth_price = await _request_eth_price(unix_ts)  # type: ignore
        if not eth_price:
            return {}

        asyncio.create_task(_cache_eth_price(unix_ts, eth_price))

    return eth_price


async def _request_eth_price(unix_ts: int) -> dict[str, dict[str, dict[str, float]]]:
    """
        Assuming that we need only hourly prices:
        1. Round timestamp
        2. Query
    """
    logger.info(f"Requesting eth price from Coingecko for {unix_ts}")

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            "https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range",
            params={
                "vs_currency": "usd",
                "from": unix_ts,
                "to": unix_ts + 3600,
            },
        )
        resp.raise_for_status()

    eth_price = resp.json()["prices"][0][1]
    logger.info(f"Received eth price for {unix_ts}: ${eth_price}")
    return eth_price


async def _cache_eth_price(unix_ts: int, eth_price) -> None:
    await redis.set_redis_key(
        RedisData(
            key=redis.get_eth_price_key(unix_ts),
            value=str(eth_price),
            # ttl=datetime.timedelta(minutes=10),
        )
    )