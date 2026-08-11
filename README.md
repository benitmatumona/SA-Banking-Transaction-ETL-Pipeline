# 🇿🇦 SA Banking Transaction ETL Pipeline

A production-style Data Engineering project that simulates a South African banking system. The project generates realistic banking data, loads it into PostgreSQL through an ETL pipeline, orchestrates workflows with Apache Airflow, and performs analytical SQL queries. It is designed to demonstrate the complete data engineering lifecycle while serving as a stepping stone toward Machine Learning Engineering.

---

# 🚀 Project Goals

- Generate realistic South African banking data.
- Build a normalized PostgreSQL database.
- Create an ETL pipeline using Python.
- Validate data before loading.
- Automate workflows with Apache Airflow.
- Perform business analytics using SQL.
- Follow production-ready project structure and coding practices.

---

# 🛠️ Tech Stack

- Python 3.10+
- Pandas
- Faker
- PostgreSQL
- SQL
- Apache Airflow
- Docker
- uv (dependency management)
- pytest, mypy, ruff
- Git
- GitHub

---

# 📂 Project Structure

```text
SA-Banking-Transaction-ETL-Pipeline/
│
├── airflow/
│   └── bank_etl_dag.py
│
├── data/
│   └── raw/
│       ├── customers.csv
│       ├── accounts.csv
│       └── transactions.csv
│
├── data_generator/
│   ├── generate_customers.py
│   ├── generate_accounts.py
│   └── generate_transactions.py
│
├── database/
│   ├── create_database.sql
│   ├── create_tables.sql
│   └── indexes.sql
│
├── docs/
│   ├── architecture.png
│   └── erd.png
│
├── sql/
│   └── analytics/
│       ├── customer_segmentation.sql
│       ├── fraud_detection.sql
│       ├── dormant_accounts.sql
│       ├── province_revenue.sql
│       ├── top_spenders.sql
│       └── monthly_revenue.sql
│
├── src/
│   ├── config.py
│   └── etl/
│       ├── load.py
│       └── validate.py
│
├── tests/
│   ├── test_load_to_postgres.py
│   └── test_validate_data.py
│
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# 🏦 Database Design

## Customers

| Column | Description |
|----------|-------------|
| customer_id | Primary key |
| full_name | Customer full name |
| province | South African province |
| join_date | Date customer joined the bank |

---

## Accounts

| Column | Description |
|----------|-------------|
| account_id | Primary key |
| customer_id | Foreign key to Customers |
| account_type | Cheque, Savings, Credit or Business |
| open_date | Account opening date |

---

## Transactions

| Column | Description |
|----------|-------------|
| transaction_id | Primary key |
| account_id | Foreign key to Accounts |
| transaction_date | Transaction date |
| transaction_type | Deposit, Withdrawal, Card Purchase, EFT, Salary |
| transaction_channel | ATM, Branch, POS, Online, Online Banking or Mobile App |
| merchant_name | Merchant involved |
| amount | Transaction amount |
| reference | Transaction reference |
| balance_after_transaction | Running account balance |
| is_fraud | Fraud indicator |

The schema is created via `database/create_database.sql` and `database/create_tables.sql`, with supporting indexes defined in `database/indexes.sql` (province, customer_id, account_id, transaction_date, is_fraud).

---

# 📈 Data Generation

The `data_generator/` scripts create realistic banking data including:

- **Customers** — 1,000 customers with South African names, provinces and join dates.
- **Accounts** — Each customer holds 1–3 accounts (Cheque, Savings, Credit or Business).
- **Transactions** — Deposits, withdrawals, card purchases, EFTs and salary payments per account.

Business rules enforced during generation and validation:

- Accounts cannot be opened before a customer joins the bank.
- Transactions cannot occur before an account is opened.
- Each customer can have between 1 and 3 accounts.
- Each account contains multiple transactions.
- Fraudulent transactions are randomly flagged via `is_fraud`.
- Transaction references and channels are generated according to transaction type.

Run the generators in order to (re)build the raw CSVs in `data/raw/`:

```bash
uv run python data_generator/generate_customers.py
uv run python data_generator/generate_accounts.py
uv run python data_generator/generate_transactions.py
```

---

# 🔄 ETL Pipeline

Implemented in `src/etl/`:

- **`validate.py`** — Validates the raw data before loading: duplicate checks, missing-value checks, allowed-value checks (province, account type, transaction type/channel), foreign-key integrity between customers → accounts → transactions, transaction amount bounds, and transaction-date consistency (a transaction can't predate its account's open date or occur in the future).
- **`load.py`** — Reads the validated CSVs with pandas, connects to PostgreSQL via `psycopg2`, and bulk-loads customers, accounts and transactions using `execute_values` for efficient batched inserts.

Pipeline steps:

1. Read the generated CSV files from `data/raw/`.
2. Validate the data (`validate()`).
3. Connect to PostgreSQL.
4. Load customers.
5. Load accounts.
6. Load transactions.
7. Commit the transaction.
8. Handle and log database errors.
9. Close the database connection.

Run it directly with:

```bash
uv run python -m src.etl.validate
uv run python -m src.etl.load
```

---

# 🔁 Orchestration (Apache Airflow)

`airflow/bank_etl_dag.py` defines a `bank_etl_dag` DAG that chains the pipeline into two tasks:

1. `validate_data` — reads the raw CSVs and runs the validation checks.
2. `load_data` — reads the raw CSVs and loads them into PostgreSQL.

The DAG is scheduled to run `@daily` and is tagged `banking`, `etl`.

---

# 🐳 Running PostgreSQL with Docker

`docker-compose.yml` spins up a PostgreSQL 16 container (`sa_banking_postgres`) and automatically applies `database/create_tables.sql` and `database/indexes.sql` on first start:

```bash
docker compose up -d
```

Default connection settings (see `src/config.py`):

| Setting | Value |
|---------|-------|
| Host | localhost |
| Port | 5432 |
| Database | south_africa_bank |
| User | postgres |

---

# 📊 Analytics

`sql/analytics/` holds the queries that will answer business questions such as:

- Customer segmentation by province
- Monthly revenue
- Fraud detection
- Dormant accounts
- Top spending customers
- Provincial revenue analysis

These files are scaffolded and are the next piece of work to be written (see **Current Progress** below).

---

# ✅ Tests

Unit tests live in `tests/` and cover the ETL layer:

- `test_load_to_postgres.py` — connection setup, bulk insert calls, and load orchestration (using mocked `psycopg2`).
- `test_validate_data.py` — each validation rule (duplicates, missing values, allowed types, transaction amounts/dates, foreign keys).

Run the test suite with:

```bash
uv run pytest
```

---

# 📚 Skills Demonstrated

## Python

- File handling
- Data structures
- Functions
- Error handling
- Modular programming
- Type hints

## Pandas

- Reading CSV files
- Data transformation
- Data validation
- DataFrame manipulation

## SQL

- Database creation
- Table creation
- Primary Keys
- Foreign Keys
- NOT NULL constraints
- Indexes
- Joins
- Aggregations
- Window functions

## PostgreSQL

- Database design
- Constraints
- Indexing
- Query optimization

## Data Engineering

- ETL pipelines
- Data validation
- Data modeling
- Data loading
- Workflow automation

## DevOps

- Docker
- Git
- GitHub
- Apache Airflow
- uv for dependency and environment management

---

# 🎯 Learning Objectives

This project demonstrates the skills expected from a Junior Data Engineer while building the foundation required for Machine Learning Engineering.

Topics covered include:

- Relational database design
- ETL development
- Data quality validation
- Workflow orchestration
- SQL analytics
- Production project organization

---

# 🚧 Current Progress

## ✅ Completed

- Customer, account and transaction data generators
- PostgreSQL database creation, schema and indexes
- Dockerized PostgreSQL setup
- ETL data validation module
- ETL load module (bulk insert into PostgreSQL)
- Airflow DAG orchestrating validation and load
- Automated tests for the ETL layer
- Project migrated to `uv` for dependency management

## 🚧 In Progress

- SQL analytics queries (files scaffolded in `sql/analytics/`, not yet written)

## ⏳ Planned

- Documentation screenshots
- Architecture diagram
- Entity Relationship Diagram (ERD)

---

# ▶️ Future Improvements

- Incremental loading
- Environment variables (.env) instead of hardcoded config values
- Logging improvements and structured logs
- Retry mechanisms
- CI/CD pipeline
- Data quality reporting
- Cloud deployment (AWS/GCP/Azure)

---

# 👨‍💻 Author

**Benit Polvie Matumona**

Aspiring Machine Learning Engineer building production-style Data Engineering projects as a foundation for advanced ML systems.
