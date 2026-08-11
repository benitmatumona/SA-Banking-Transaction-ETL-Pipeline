cat > README.md << 'README_EOF'
# 🇿🇦 SA Banking Transaction ETL Pipeline

A production-style Data Engineering project that simulates a South African banking system. The project generates realistic banking data, validates it, loads it into PostgreSQL through an ETL pipeline, orchestrates workflows with Apache Airflow, and performs analytical SQL queries. It is designed to demonstrate the complete data engineering lifecycle while serving as a stepping stone toward Machine Learning Engineering.

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

- Python (managed with [uv](https://docs.astral.sh/uv/))
- Pandas
- Faker
- PostgreSQL
- psycopg2
- SQL
- Apache Airflow
- Docker / Docker Compose
- pytest
- ruff + mypy
- Git / GitHub

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
│       ├── dormant_accounts.sql
│       ├── fraud_detection.sql
│       ├── monthly_revenue.sql
│       ├── province_revenue.sql
│       └── top_spenders.sql
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
├── .python-version
├── .gitignore
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
| transaction_channel | ATM, Branch, POS, Online, Mobile App, etc. |
| merchant_name | Merchant involved |
| amount | Transaction amount |
| reference | Transaction reference |
| balance_after_transaction | Running account balance |
| is_fraud | Fraud indicator |

---

# 📈 Data Generation

The project creates realistic banking data including:

- Customers
- Accounts
- Transactions

Business rules include:

- Accounts cannot be opened before a customer joins the bank.
- Transactions cannot occur before an account is opened.
- Each customer can have between 1 and 3 account types.
- Each account contains multiple transactions.
- Fraudulent transactions are randomly generated.
- Transaction references are generated according to transaction type.

Run the generators in order (each one reads the previous CSV):

```bash
python data_generator/generate_customers.py
python data_generator/generate_accounts.py
python data_generator/generate_transactions.py
```

---

# 🔄 ETL Pipeline

The ETL pipeline performs the following steps:

1. Read generated CSV files (`src/etl/load.py::read_data`).
2. Validate the data (`src/etl/validate.py::validate`).
3. Connect to PostgreSQL.
4. Load Customers.
5. Load Accounts.
6. Load Transactions.
7. Commit the transaction.
8. Handle errors.
9. Close the database connection.

Run validation and loading directly:

```bash
python -m src.etl.validate
python -m src.etl.load
```

Or let Airflow orchestrate both steps via `airflow/bank_etl_dag.py`, which validates the data before loading it into PostgreSQL.

---

# 🐳 Running PostgreSQL with Docker

A ready-to-use `docker-compose.yml` spins up PostgreSQL and creates the schema automatically on first boot:

```bash
docker compose up -d
```

This starts Postgres on `localhost:5432`, creates the `south_africa_bank` database, and runs `database/create_tables.sql` and `database/indexes.sql` on initialization.

> Update the `DB_USER`, `DB_PASSWORD`, `DB_NAME` and `DB_HOST` values in `src/config.py` to match the credentials in `docker-compose.yml` (or move them to environment variables) before running the ETL pipeline.

---

# 📊 Analytics

The project answers business questions such as (see `sql/analytics/`):

- Customer segmentation by province — `customer_segmentation.sql`
- Monthly revenue trends — `monthly_revenue.sql`
- Fraud detection — `fraud_detection.sql`
- Dormant accounts — `dormant_accounts.sql`
- Top spending customers — `top_spenders.sql`
- Provincial revenue analysis — `province_revenue.sql`

---

# ✅ Testing

Unit tests cover both the validation logic and the load logic (with the database mocked, so no live Postgres instance is required):

```bash
uv run pytest tests/ -v
```

---

# 📚 Skills Demonstrated

## Python

- File handling
- Data structures
- Functions
- Error handling
- Modular programming

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

- Docker / Docker Compose
- Git
- GitHub
- Apache Airflow
- Automated testing (pytest)

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

- Customer data generator
- Account data generator
- Transaction data generator
- PostgreSQL database creation
- Database schema
- Database indexes
- ETL pipeline (`validate.py`, `load.py`)
- Data validation
- Airflow DAG
- SQL analytics queries
- Automated tests
- Dockerized PostgreSQL

## ⏳ Planned

- Documentation screenshots
- Architecture diagram
- Entity Relationship Diagram (ERD)
- Incremental loading
- Environment variables (`.env`)
- Logging
- Retry mechanisms
- CI/CD pipeline

---

# ▶️ Future Improvements

- Incremental loading
- Environment variables (`.env`) for database credentials
- Logging
- Retry mechanisms
- CI/CD pipeline
- Data quality reporting
- Cloud deployment (AWS/GCP/Azure)

---

# 👨‍💻 Author

**Benit Polvie Matumona**

Aspiring Machine Learning Engineer building production-style Data Engineering projects as a foundation for advanced ML systems.
README_EOF
