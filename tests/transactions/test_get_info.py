import csv
import pytest
from async_asgi_testclient import TestClient

TEST_TX_DATA = {
    "hash": "0x8d7642ea82f1963ee846b32929ab2f027e87ee28be8aec28f4eaa37c389b86f9", 
    "nonce": "0", 
    "block_hash": "0x21521204d6579c54759afe975b0dcbbede9ebea48473fe2a8f7719be5cc5d320", 
    "block_number": "17818510", 
    "transaction_index": "49", 
    "from_address": "0xe0ae9723c3776868e7793bb99a758edebcda56b3", 
    "to_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", 
    "value": "0", "gas": "90000", "gas_price": "19000000000", 
    "block_timestamp": "2023-08-01 06:58:35.000000 UTC", 
    "max_fee_per_gas": "", "max_priority_fee_per_gas": "", 
    "transaction_type": "0", "receipts_cumulative_gas_used": "3326876", 
    "receipts_gas_used": "43713", "receipts_contract_address": "", 
    "receipts_root": "", "receipts_status": "1", 
    "receipts_effective_gas_price": "19000000000"
}

@pytest.mark.asyncio
async def test_get_tx_info(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:

    # upload test tx data
    resp = await client.post(f"/transactions/", json=TEST_TX_DATA)
    assert resp.status_code == 200

    # get data from service
    tx_hash = TEST_TX_DATA["hash"]
    resp = await client.get(f"/transactions/{tx_hash}")
    assert resp.status_code == 200

    tx_data = resp.json()
    assert tx_data["hash"] == tx_hash
    assert tx_data["gas_used_gwei"] is not None

    # should we wait 1 sec to parse Coingecko?
    assert tx_data["gas_used_usd"] is not None
    
