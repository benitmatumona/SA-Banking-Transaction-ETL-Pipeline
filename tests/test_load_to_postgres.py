from unittest.mock import MagicMock, patch

import pandas as pd

from src.etl.load import bulk_insert, connect, load, load_table


def test_connect_calls_psycopg2_with_expected_arguments() -> None:
    with patch("src.etl.load.psycopg2.connect") as mock_connect:
        connect("mydb", "myuser", "mypass", "myhost")
        mock_connect.assert_called_once_with(
            dbname="mydb", user="myuser", password="mypass", host="myhost"
        )


def test_bulk_insert_calls_execute_values_with_expected_arguments() -> None:
    cur = MagicMock()
    rows = [(1, "a"), (2, "b")]
    sql = "INSERT INTO table VALUES %s"

    with patch("src.etl.load.execute_values") as mock_execute_values:
        bulk_insert(cur=cur, sql=sql, rows=rows)
        mock_execute_values.assert_called_once_with(
            cur=cur, sql=sql, rows=rows, page_size=1000
        )


def test_load_table_converts_dataframe_rows_and_calls_bulk_insert() -> None:
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    cur = MagicMock()
    sql = "INSERT INTO table VALUES %s"

    with patch("src.etl.load.bulk_insert") as mock_bulk_insert:
        load_table(df, cur, sql)
        mock_bulk_insert.assert_called_once_with(
            cur=cur, sql=sql, rows=[(1, "x"), (2, "y")]
        )


def test_load_commits_when_no_error_occurs() -> None:
    customers_df = pd.DataFrame({"customer_id": [1], "full_name": ["Test"]})
    accounts_df = pd.DataFrame({"account_id": [1], "customer_id": [1]})
    transactions_df = pd.DataFrame({"transaction_id": [1], "account_id": [1]})

    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch("src.etl.load.connect", return_value=mock_conn) as mock_connect, \
         patch("src.etl.load.load_table") as mock_load_table:
        load(customers_df, accounts_df, transactions_df)

        mock_connect.assert_called_once()
        assert mock_load_table.call_count == 3


def test_load_handles_database_error_without_raising() -> None:
    import psycopg2

    customers_df = pd.DataFrame({"customer_id": [1]})
    accounts_df = pd.DataFrame({"account_id": [1]})
    transactions_df = pd.DataFrame({"transaction_id": [1]})

    with patch("src.etl.load.connect", side_effect=psycopg2.Error("boom")):
        load(customers_df, accounts_df, transactions_df)
