from fastapi import APIRouter

from src.transactions import service
from src.transactions.exceptions import TransactionNotFound
from src.transactions.schemas import TransactionCompactResponse, TransactionInsert

router = APIRouter()


@router.get(
    "/{hash}",
    response_model=TransactionCompactResponse,
)
async def get_transaction_by_hash(tx_hash: str) -> TransactionCompactResponse:
    requested_tx = await service.get_transaction_by_hash(tx_hash)

    if not requested_tx:
        raise TransactionNotFound()

    return TransactionCompactResponse(requested_tx)


@router.post(
    "/{hash}",
    response_model=TransactionCompactResponse,
)
async def save_transaction_data(transaction_data: TransactionInsert) -> None:
    await service.insert_transaction_data(transaction_data)

    # from_address: str
    # to_address: str
    # block_number: int
    # gas_used: int


#     {
#   "hash": "0xaaaaa",
#   "fromAddress": "0x000000",
#   "toAddress": "0x000001",
#   "blockNumber": 1234,
#   "executedAt": "Jul-04-2022 12:02:24 AM +UTC",
#   "gasUsed": 12345678,
#   "gasCostInDollars": 4.23,
# }
