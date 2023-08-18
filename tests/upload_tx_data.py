"""
    Script which uploads transactions. 
    For manual testing purposes only.
"""

import csv
import httpx

FILEPATH = "./tests/data/ethereum_txs.csv"

print(f"I'm going to upload transactions from {FILEPATH} by querying POST /transactions endpoint for each transaction.")
print(f"You can open http://localhost:8000/docs to check /stats endpoint.")

with open(FILEPATH, "r") as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        r = httpx.post(
            "http://localhost:8000/transactions/",
            json=row,
        )
        if r.status_code != 200:
            print(row)
            print(r.text)
