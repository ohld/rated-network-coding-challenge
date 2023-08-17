import csv
import json

import httpx

with open("./tests/data/ethereum_txs.csv", "r") as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        print(json.dumps(row))
        _ = httpx.post(
            "http://localhost:8000/transactions/",
            json=row,
        )
