import csv

import requests

with open("./tests/data/ethereum_txs.csv", 'r') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        r = requests.post(
            "http://0.0.0.0:8000",
            data=row,
        )