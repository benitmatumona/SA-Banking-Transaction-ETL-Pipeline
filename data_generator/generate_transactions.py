import random
import itertools
import os
import pandas as pd
from typing import Any
from faker import Faker
from src.config import TRANSACTION_CHANNELS, TRANSACTION_TYPES, MERCHANTS


def generate_transactions(
    data: pd.DataFrame,
    fake: Faker,
    transaction_id: itertools.count,
) -> pd.DataFrame:
    new_data: dict[str, list[Any]] = {
        "transaction_id": [],
        "account_id": [],
        "transaction_date": [],
        "transaction_type": [],
        "transaction_channel": [],
        "merchant_name": [],
        "amount": [],
        "reference": [],
        "balance_after_transaction": [],
        "is_fraud": [],
    }

    for row in data.itertuples():
        random_number_of_transactions = random.randint(3, 10)
        end_date = pd.Timestamp.today()
        balance = random_number_of_transactions * 5001

        for _ in range(random_number_of_transactions):
            balance = generate_transaction(
                new_data,
                row,
                fake,
                transaction_id,
                end_date,
                balance,
                TRANSACTION_TYPES,
                TRANSACTION_CHANNELS,
                MERCHANTS,
            )

    return pd.DataFrame(new_data)


def generate_transaction(
    df: dict[str, list[Any]],
    row: Any,
    fake: Faker,
    transaction_id: itertools.count,
    end_date: pd.Timestamp,
    balance: int,
    transaction_types: dict[str, str],
    transaction_channels: dict[str, list[str]],
    merchants: dict[str, list[str]],
) -> int:
    transaction_type, transaction_channel = generate_transaction_info(
        transaction_types,
        transaction_channels,
    )

    amount = generate_amount()

    merchant_name = random.choice(merchants[transaction_type])

    reference = generate_reference(
        transaction_types,
        transaction_type,
        merchant_name,
    )

    fraud_flag = is_fraud(
        amount,
        transaction_channel,
        transaction_type,
        merchant_name,
    )

    updated_balance = update_balance(balance, amount, transaction_type)

    write_row(
        df,
        row,
        fake,
        transaction_id,
        transaction_type,
        transaction_channel,
        merchant_name,
        reference,
        amount,
        end_date,
        updated_balance,
        fraud_flag,
    )

    return updated_balance


def generate_transaction_info(
    transaction_types: dict[str, str],
    transaction_channels: dict[str, list[str]],
) -> tuple[str, str]:
    transaction_type = random.choice(tuple(transaction_types.keys()))
    transaction_channel = random.choice(transaction_channels[transaction_type])
    return transaction_type, transaction_channel


def generate_amount() -> int:
    return random.choices(
    population=[
        random.randint(20, 300),
        random.randint(301, 1000),
        random.randint(1001, 5000),
    ],
    weights=[70, 25, 5],
    )[0]


def generate_reference(
    transaction_types: dict[str, list[str]],
    transaction_column: str,
    merchant_name: str,
) -> str:
    reference = transaction_types[transaction_column].replace(
        "merchant_name", merchant_name
    )

    return (
        "EFT DEPOSIT"
        if reference == "CASH DEPOSIT" and random.random() > 0.5
        else reference
    )


def is_fraud(
    amount: int,
    transaction_channel: str,
    transaction_type: str,
    merchant_name: str,
) -> bool:
    if amount > 4500 and transaction_channel == "ATM":
        fraud_flag = random.random() <= 0.20
    elif (
        transaction_type == "Card Purchase"
        and merchant_name == "Uber"
        and amount > 3000
    ):
        fraud_flag = random.random() <= 0.12
    else:
        fraud_flag = random.random() <= 0.02
    return fraud_flag


def update_balance(
    balance: int,
    amount: int,
    transaction_type: str,
) -> int:
    is_incoming = random.random() >= 0.5

    if transaction_type in ("Salary", "Deposit"):
        balance += amount
    elif transaction_type == "EFT":
        if is_incoming:
            balance += amount
        else:
            balance -= amount
    else:
        balance -= amount

    return balance


def write_row(
    df: dict,
    row,
    fake,
    transaction_id: itertools.count,
    transaction_type,
    transaction_channel,
    merchant_name,
    reference,
    amount,
    end_date,
    balance,
    fraud_flag,
):
    df["transaction_id"].append(next(transaction_id))
    df["account_id"].append(row.account_id)
    df["transaction_date"].append(
        fake.date_time_between(row.open_date, end_date)
    )
    df["transaction_type"].append(transaction_type)
    df["transaction_channel"].append(transaction_channel)

    df["merchant_name"].append(
        merchant_name if transaction_type != "Salary" else "Employer"
    )

    df["amount"].append(amount)
    df["reference"].append(reference)
    df["balance_after_transaction"].append(balance)
    df["is_fraud"].append(fraud_flag)


def generate_transactions_file():

    os.makedirs("data/raw", exist_ok=True)
    data = pd.read_csv(
        "data/raw/accounts.csv",
        parse_dates=["open_date"]
    )
    fake = Faker()
    transaction_id = itertools.count(start=300001)
    generated_df = generate_transactions(
        data=data, 
        fake=fake, 
        transaction_id=transaction_id
    )
    generated_df.to_csv(
        "data/raw/transactions.csv", 
        index=False
    )


if __name__ == "__main__":
    generate_transactions_file()
