"""
Airflow DAG that orchestrates the SA Banking Transaction ETL pipeline:
read the raw CSVs, validate them, and load them into PostgreSQL.
"""
from __future__ import annotations

import datetime

from airflow.decorators import dag, task

from src.etl.load import load, read_data
from src.etl.validate import validate


@dag(
    dag_id="bank_etl_dag",
    description="Validate and load SA banking transaction data into PostgreSQL.",
    schedule="@daily",
    start_date=datetime.datetime(2026, 1, 1),
    catchup=False,
    tags=["banking", "etl"],
)
def bank_etl_dag() -> None:
    @task
    def validate_data() -> None:
        """Read the raw CSV files and validate them before loading."""
        customers_df, accounts_df, transactions_df = read_data()
        validate(customers_df, accounts_df, transactions_df)

    @task
    def load_data() -> None:
        """Read the raw CSV files and load them into PostgreSQL."""
        customers_df, accounts_df, transactions_df = read_data()
        load(customers_df, accounts_df, transactions_df)

    validate_data() >> load_data()


bank_etl_dag()
