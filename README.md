# Rated Network Coding Challenge
Original repo with task description: https://github.com/rated-network/coding-challenge/

Built with [FastAPI best practices](https://github.com/zhanymkanov/fastapi-best-practices) in mind using [FastAPI production template](https://github.com/zhanymkanov/fastapi_production_template).

# Quick start

``` bash

git clone https://github.com/ohld/rated-network-coding-challenge
cd rated-network-coding-challenge

cp .env.example .env
docker network create app_main
docker-compose up -d --build

# apply migrations & upload sample data
docker compose exec app migrate
docker compose exec app python ./tests/upload_tx_data.py
```


## What's inside

### GET `/stats` (src/stats/router.py)

``` json
{
  "total_transactions_in_db": 5000,
  "total_gas_used_gwei": 10492553722.431274,
  "total_gas_cost_in_usd": 19219.824439832475
}
```

### POST `/transactions` (src/transactions/router.py)

Creates transaction in db, returns nothing (for simplicity). Boilerplate to integrate streams further. 
1. Stores raw data
2. Calculates `gas_used_gwei` on the fly
3. Background task to calculate `gas_used_usd` using Coingecko API (cached with Redis)

### GET `/transactions/{tx_hash}` (src/transactions/router.py)

Returns TransactionCompactResponse:
``` json
{
  "hash": "0x06568e8d3c76f6961c650c3b2c9404c79b3bb14138051313b9a74e6255d02140",
  "from_address": "0x7f21c6ab63892ed9db38f5b79d0fadaf4ec79a42",
  "to_address": "0x7a097dbacb237d6b6a047368f43514992510bb79",
  "block_number": 17818510,
  "block_timestamp": "2023-08-01T06:58:35+0000",
  "gas_used_gwei": 399397.655979,
  "gas_used_usd": 0.7305556709464458
}
```

### Tests

1. tx data upload + proper get response with calculated fields (`gas_used_gwei`, `gas_used_usd`)
2. txs data upload from csv file + proper /stats response

I didn't test the Coingecko API integration and didn't write fallbacks in case it will not be available at some point.


## Local Development

### First Build Only
1. `cp .env.example .env`
2. `docker network create app_main`
3. `docker-compose up -d --build`

### Linters
Format the code
```shell
docker compose exec app format
```

### Migrations
- Create an automatic migration from changes in `src/database.py`
```shell
docker compose exec app makemigrations *migration_name*
```
- Run migrations
```shell
docker compose exec app migrate
```
- Downgrade migrations
```shell
docker compose exec app downgrade -1  # or -2 or base or hash of the migration
```
### Tests
All tests are integrational and require DB connection. 

One of the choices I've made is to use default database (`postgres`), separated from app's `app` database.
- Using default database makes it easier to run tests in CI/CD environments, since there is no need to setup additional databases
- Tests are run with `force_rollback=True`, i.e. every transaction made is then reverted

Run tests
```shell
docker compose exec app pytest
```
