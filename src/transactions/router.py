from fastapi import APIRouter, BackgroundTasks

from src.transactions import service
from src.transactions.exceptions import TransactionNotFound
from src.transactions.schemas import TransactionCompactResponse, TransactionInsert

router = APIRouter()


@router.get(
    "/{tx_hash}",
    response_model=TransactionCompactResponse,
)
async def get_transaction_by_hash(tx_hash: str) -> TransactionCompactResponse:
    requested_tx = await service.get_transaction_by_hash(tx_hash)

    if not requested_tx:
        raise TransactionNotFound()

    return TransactionCompactResponse.parse_obj(requested_tx)


# TODO: proper response scheme according to bis req
@router.post(
    "/",
)
async def save_transaction_data(
    data: TransactionInsert,
    worker: BackgroundTasks,
) -> None:
    await service.insert_transaction_data(data)

    worker.add_task(
        service.calculate_transaction_gas_used_usd,
        data.hash,
        data.block_timestamp,
        data.gas_used_gwei,
    )
