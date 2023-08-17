import csv
import pytest
from async_asgi_testclient import TestClient


@pytest.mark.asyncio
async def test_upload_bulk(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    tx_hashes = set()  # duplicates in test data
    with open("./tests/data/ethereum_txs.csv", "r") as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            resp = await client.post(
                "/transactions/",
                json=row,
            )

            assert resp.status_code == 200
            tx_hashes.add(row["hash"])
            # endpoint returns nothing -> no tests on resp.json()

    # TODO: move stats tests to separate file    
    resp = await client.get("/stats")
    assert resp.status_code == 200

    stats_data = resp.json()
    assert stats_data["total_transactions_in_db"] >= len(tx_hashes)

            
