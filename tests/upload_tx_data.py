"""
    Script which uploads transactions. 
    For manual testing purposes only.
"""

import csv
import httpx

with open("./tests/data/ethereum_txs.csv", "r") as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        r = httpx.post(
            "http://localhost:8000/transactions/",
            json=row,
        )
        if r.status_code != 200:
            print(row)
            print(r.text)
