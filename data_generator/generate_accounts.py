import random
import os
import itertools
import pandas as pd
from typing import Any
from faker import Faker
from src.config import ACCOUNT_TYPES


os.makedirs("data/raw", exist_ok=True)
data = pd.read_csv(
    "data/raw/customers.csv",
    parse_dates=["join_date"]
    )
fake = Faker()
account_id = itertools.count(start=200001)


new_data: dict[str, list[Any]] = {"account_id": [], "customer_id": [], "account_type": [], "open_date": []}

for row in data.itertuples():
    random_number_of_accounts = random.randint(1, 3)
    random_accounts = random.sample(ACCOUNT_TYPES, random_number_of_accounts)

    for account_type in random_accounts:
        start_date = row.join_date
        end_date = pd.Timestamp.today()
        open_date = fake.date_between(start_date, end_date)
        new_data["account_id"].append(next(account_id))
        new_data["customer_id"].append(row.customer_id)
        new_data["account_type"].append(account_type)
        new_data["open_date"].append(open_date)

df = pd.DataFrame(new_data)
df.to_csv("data/raw/accounts.csv", index=False)
