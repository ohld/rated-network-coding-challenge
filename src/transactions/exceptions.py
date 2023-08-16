from src.exceptions import NotFound

from .constants import ErrorCode


class TransactionNotFound(NotFound):
    DETAIL = ErrorCode.TRANSACTION_NOT_FOUND
