import csv
import json

import requests

with open("./tests/data/ethereum_txs.csv", 'r') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        print(json.dumps(row))
        r = requests.post(
            "http://localhost:8000/transactions/",
            json=row,
        )