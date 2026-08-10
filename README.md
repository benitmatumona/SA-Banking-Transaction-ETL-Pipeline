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

- Python
- Pandas
- Faker
- PostgreSQL
- SQL
- Apache Airflow
- Docker
- Git
- GitHub

---

# 📂 Project Structure

```text
SA-FINANCE-LAKEHOUSE/
│
├── airflow/
│   └── bank_etl_dag.py
│
├── analytics/
│   ├── customer_segmentation.sql
│   ├── fraud_detection.sql
│   ├── dormant_accounts.sql
│   ├── province_revenue.sql
│   ├── top_spenders.sql
│   └── monthly_revenue.sql
│
├── data/
│   ├── raw/
│   └── processed/
│
├── data_generation/
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
│   ├── erd.png
│   └── screenshots/
│
├── etl/
│   ├── load_to_postgres.py
│   └── validate_data.py
│
├── tests/
│   ├── test_load_to_postgres.py
│   └── test_validate_data.py
│
├── README.md
├── requirements.txt
└── docker-compose.yml
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
| account_type | Cheque, Savings or Credit |
| open_date | Account opening date |

---

## Transactions

| Column | Description |
|----------|-------------|
| transaction_id | Primary key |
| account_id | Foreign key to Accounts |
| transaction_date | Transaction date |
| transaction_type | Deposit, Withdrawal, Card Purchase, EFT, Salary |
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

---

# 🔄 ETL Pipeline

The ETL pipeline performs the following steps:

1. Read generated CSV files.
2. Validate the data.
3. Connect to PostgreSQL.
4. Load Customers.
5. Load Accounts.
6. Load Transactions.
7. Commit the transaction.
8. Handle errors.
9. Close database connection.

---

# 📊 Analytics

The project answers business questions such as:

- Customer segmentation by province
- Monthly revenue
- Fraud detection
- Dormant accounts
- Top spending customers
- Provincial revenue analysis

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

- Docker
- Git
- GitHub
- Apache Airflow

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

## 🚧 In Progress

- ETL pipeline
- Data validation

## ⏳ Planned

- Airflow DAG
- SQL analytics
- Automated tests
- Documentation screenshots
- Architecture diagram
- Entity Relationship Diagram (ERD)

---

# ▶️ Future Improvements

- Incremental loading
- Environment variables (.env)
- Dockerized PostgreSQL
- Logging
- Retry mechanisms
- CI/CD pipeline
- Data quality reporting
- Cloud deployment (AWS/GCP/Azure)

---

# 👨‍💻 Author

**Benit Polvie Matumona**

Aspiring Machine Learning Engineer building production-style Data Engineering projects as a foundation for advanced ML systems.
