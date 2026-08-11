import pandas as pd
import pytest

from src.etl.validate import (
    check_allowed_types,
    check_duplicates,
    check_foreign_keys,
    check_missing_values,
    check_transaction_amounts,
    check_transaction_dates,
    validate,
)


@pytest.fixture
def customers_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_id": [100001, 100002],
            "full_name": ["Thabo Mokoena", "Sarah van der Merwe"],
            "province": ["Gauteng", "Western Cape"],
            "join_date": ["2021-01-01", "2021-06-15"],
        }
    )


@pytest.fixture
def accounts_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "account_id": [200001, 200002],
            "customer_id": [100001, 100002],
            "account_type": ["Cheque", "Savings"],
            "open_date": pd.to_datetime(["2021-02-01", "2021-07-01"]),
        }
    )


@pytest.fixture
def transactions_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "transaction_id": [300001, 300002],
            "account_id": [200001, 200002],
            "transaction_date": pd.to_datetime(["2021-03-01", "2021-08-01"]),
            "transaction_type": ["Deposit", "Card Purchase"],
            "transaction_channel": ["ATM", "POS"],
            "merchant_name": ["This Bank", "Checkers"],
            "amount": [1500.0, 250.5],
            "reference": ["CASH DEPOSIT", "Checkers"],
            "balance_after_transaction": [1500, 1750],
            "is_fraud": [False, False],
        }
    )


def test_check_duplicates_passes_with_unique_values(customers_df: pd.DataFrame) -> None:
    assert check_duplicates(customers_df, "customer_id") is True


def test_check_duplicates_raises_on_duplicate_values(customers_df: pd.DataFrame) -> None:
    duplicated = pd.concat([customers_df, customers_df.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError, match="Duplicate values"):
        check_duplicates(duplicated, "customer_id")


def test_check_missing_values_passes(customers_df: pd.DataFrame) -> None:
    assert check_missing_values(customers_df, ["customer_id", "full_name"]) is True


def test_check_missing_values_raises_on_null(customers_df: pd.DataFrame) -> None:
    customers_df.loc[0, "full_name"] = None
    with pytest.raises(ValueError, match="Missing values"):
        check_missing_values(customers_df, ["full_name"])


def test_check_allowed_types_passes(customers_df: pd.DataFrame) -> None:
    assert check_allowed_types(
        customers_df, "province", ["Gauteng", "Western Cape"]
    ) is True


def test_check_allowed_types_raises_on_invalid_value(customers_df: pd.DataFrame) -> None:
    customers_df.loc[0, "province"] = "Narnia"
    with pytest.raises(ValueError, match="Invalid province"):
        check_allowed_types(customers_df, "province", ["Gauteng", "Western Cape"])


def test_check_transaction_amounts_passes(transactions_df: pd.DataFrame) -> None:
    assert check_transaction_amounts(transactions_df) is True


def test_check_transaction_amounts_raises_on_negative_amount(
    transactions_df: pd.DataFrame,
) -> None:
    transactions_df.loc[0, "amount"] = -10
    with pytest.raises(ValueError, match="greater than 0"):
        check_transaction_amounts(transactions_df)


def test_check_transaction_amounts_raises_on_amount_too_large(
    transactions_df: pd.DataFrame,
) -> None:
    transactions_df.loc[0, "amount"] = 20_000_000
    with pytest.raises(ValueError, match="10 000 000"):
        check_transaction_amounts(transactions_df)


def test_check_transaction_dates_passes(
    transactions_df: pd.DataFrame, accounts_df: pd.DataFrame
) -> None:
    assert check_transaction_dates(transactions_df, accounts_df) is True


def test_check_transaction_dates_raises_when_before_open_date(
    transactions_df: pd.DataFrame, accounts_df: pd.DataFrame
) -> None:
    transactions_df.loc[0, "transaction_date"] = pd.Timestamp("2020-01-01")
    with pytest.raises(ValueError, match="Invalid dates"):
        check_transaction_dates(transactions_df, accounts_df)


def test_check_foreign_keys_passes(
    accounts_df: pd.DataFrame, customers_df: pd.DataFrame
) -> None:
    assert check_foreign_keys(
        accounts_df, customers_df, "customer_id", "customer_id"
    ) is True


def test_check_foreign_keys_raises_on_orphan_row(
    accounts_df: pd.DataFrame, customers_df: pd.DataFrame
) -> None:
    accounts_df.loc[0, "customer_id"] = 999999
    with pytest.raises(ValueError, match="Invalid customer_id"):
        check_foreign_keys(accounts_df, customers_df, "customer_id", "customer_id")


def test_validate_passes_on_clean_data(
    customers_df: pd.DataFrame,
    accounts_df: pd.DataFrame,
    transactions_df: pd.DataFrame,
) -> None:
    validate(customers_df, accounts_df, transactions_df)


def test_validate_raises_on_dirty_data(
    customers_df: pd.DataFrame,
    accounts_df: pd.DataFrame,
    transactions_df: pd.DataFrame,
) -> None:
    transactions_df.loc[0, "amount"] = -50
    with pytest.raises(ValueError):
        validate(customers_df, accounts_df, transactions_df)
