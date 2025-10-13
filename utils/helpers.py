from datetime import datetime, timedelta
import math


def get_authorized_date(transaction):
    authorized_date = transaction.get("authorized_date")
    if authorized_date is None:
        return None
    if isinstance(authorized_date, str):
        authorized_date = datetime.strptime(authorized_date, "%Y-%m-%d").date()
    return authorized_date


def get_time_range(time_range: str):
    end_date = datetime.now()
    if time_range == "today":
        start_date = end_date - timedelta(hours=24)
    elif time_range == "yesterday":
        start_date = end_date - timedelta(days=1)
    elif time_range == "last_week":
        start_date = end_date - timedelta(days=7)
    elif time_range == "last_month":
        start_date = end_date - timedelta(days=30)
    else:
        start_date = end_date - timedelta(days=90)

    return start_date, end_date


def parse_categories(amounts_by_category, total) -> str:
    list = "\n"
    for key in amounts_by_category:
        formatted_key = key.title().replace("_", " ")
        value = amounts_by_category[key]
        formatted_value = f"${value} ({math.trunc(value/total * 100)}%)"

        list += f"• {formatted_key}: {formatted_value}\n"

    return list


def transaction_has_category(transaction, search_term: str) -> bool:
    category = transaction.get("personal_finance_category", {}).get("primary")
    # improve soft matching here
    return category and search_term.lower() in category.lower()


def transaction_has_merchant_name(transaction, search_term: str) -> bool:
    merchant = transaction.get("merchant_name")
    return merchant and search_term.lower() in merchant.lower()


def truncate(value: float) -> float:
    return int(value * (10**2)) / (10**2)


def update_env_file(key, value, env_path=".env"):
    lines = []
    found = False

    try:
        with open(env_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        pass

    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"\n{key}={value}\n"
            found = True
            break

    if not found:
        lines.append(f"\n{key}={value}\n")

    with open(env_path, "w") as file:
        file.writelines(lines)

    print(f"✅ Updated {key} in {env_path}")
