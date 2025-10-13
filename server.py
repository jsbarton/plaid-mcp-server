import os
from datetime import datetime
from mcp.server.fastmcp import Context, FastMCP
from plaid.api import plaid_api
from api.client import client, client_id, secret, get_access_token
from utils.helpers import (
    get_authorized_date,
    get_time_range,
    transaction_has_merchant_name,
    transaction_has_category,
    truncate,
    parse_categories,
)
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)

from plaid.api.plaid_api import LinkTokenCreateRequest
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products

mcp = FastMCP("Plaid Finance Inspector")


@mcp.tool()
def get_hosted_link():
    request = LinkTokenCreateRequest(
        client_id=client_id,
        client_name="Plaid MCP Server",
        country_codes=[CountryCode("US")],
        hosted_link={},
        language="en",
        products=[Products("transactions")],
        secret=secret,
        user=LinkTokenCreateRequestUser(
            client_user_id="user-id", phone_number="4155550011"
        ),
        webhook="https://overhappily-regenia-wasteless.ngrok-free.dev/hosted-link-destination",
    )
    response = client.link_token_create(request)
    return response["hosted_link_url"]


@mcp.tool()
async def get_spending_summary(time_range: str, category: str = None) -> str:
    """
    Gets spending summary for a specific time range,
    and optionally filters by category if specified

    Returns:
        Formatted spending information
    """
    try:

        start_date, end_date = get_time_range(time_range)
        access_token = os.getenv("ACCESS_TOKEN")

        transactions_response = client.transactions_sync(
            plaid_api.TransactionsSyncRequest(
                access_token=access_token, client_id=client_id, secret=secret
            )
        )

        transactions = transactions_response["added"]

        transactions_within_range = []
        total = 0
        num_transactions = 0
        amounts_by_category = {}

        for t in transactions:
            authorized_date = get_authorized_date(t)
            if authorized_date is None:
                continue

            transaction_category = t.get("personal_finance_category", {}).get("primary")

            if (
                authorized_date < end_date.date()
                and authorized_date >= start_date.date()
            ):
                amount = abs(t.get("amount")) or 0
                total += amount
                num_transactions += 1

                if category:
                    if transaction_has_category(t, category):
                        # map the category to a standard string
                        amounts_by_category[category] = (
                            (amounts_by_category.get(category) + amount)
                            if category in amounts_by_category
                            else amount
                        )
                else:
                    transaction_category = t.get("personal_finance_category", {}).get(
                        "primary"
                    )
                    amounts_by_category[transaction_category] = (
                        (amounts_by_category.get(transaction_category) + amount)
                        if transaction_category in amounts_by_category
                        else amount
                    )

                transactions_within_range.append(t)

        return f"""
📊 Spending Summary ({time_range.replace('_', ' ').title()})
{'=' * 50}

Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}
{f"Category Filter: {category}" if category else "All Categories"}

💰 Total Spending: ${truncate(total)}
📈 Transaction Count: {num_transactions}

Top Categories:
        {parse_categories(amounts_by_category=amounts_by_category, total=total)}
        """
    except Exception as e:
        # If the token has expired, prompt the user to log back in with their credentials
        return f"Error fetching transactions: {e}"


@mcp.tool()
async def get_account_balance() -> str:
    """
    Get current account balances.

    Returns:
        Formatted account balance information
    """

    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            "public-sandbox-1650c78f-7426-497e-95b7-c412391b6bd8"
        )

        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response["access_token"]

        request = AccountsBalanceGetRequest(
            access_token=access_token, client_id=client_id, secret=secret
        )
        response = client.accounts_balance_get(request)
        accounts = response["accounts"]

        accounts_list = f"""
        # 🏦 Account Balances
        # {'=' * 30}\n 
        """

        for account in accounts:
            account_name = account.get("name")
            available_balance = account.get("balances", {}).get("available")
            current_balance = account.get("balances", {}).get("current")
            account_mask = f"{'*' * 4}{account.get("mask")}"

            if all([account_name, available_balance, current_balance, account_mask]):
                accounts_list += f"""
                {account_name} ({account_mask})
                • Available: ${available_balance}
                • Current: ${current_balance}
                \n
                """
            else:
                continue

        return accounts_list

    except Exception as e:
        return f"Error getting account balance: {str(e)}"


@mcp.tool()
async def search_transactions(search_term: str, limit: int = 10) -> str:
    """
    Search for transactions by merchant name or description.

    Args:
        search_term: Term to search for in transaction names
        limit: Maximum number of transactions to return (default: 10)

    Returns:
        Formatted list of matching transactions
    """

    try:
        access_token = get_access_token(
            "public-sandbox-509e1396-fe83-4230-817a-078595e5f430"
        )
        transactions_response = client.transactions_sync(
            plaid_api.TransactionsSyncRequest(
                access_token=access_token, client_id=client_id, secret=secret
            )
        )
        transactions = transactions_response["added"]

        terms = f"""
🔍 Transaction Search Results
{'=' * 40}\n
"""
        i = 0
        for t in transactions:
            if (transaction_has_merchant_name(t, search_term)) or (
                transaction_has_category(t, search_term)
            ):
                if i < limit:
                    merchant_name = t.get("merchant_name")
                    date = t.get("date")
                    amount = t.get("amount")
                    category = t.get("personal_finance_category", {}).get("primary")

                    if all([merchant_name, date, amount, category]) != True:
                        continue
                    terms += f"""
                    {i}. {t.get("merchant_name")}
                         Date: {date}
                         Amount: -${amount}
                         Category: {category.title().replace("_", " ")}
                    """
                else:
                    break
                i += 1

        return terms

    except Exception as e:
        return f"Error searching transactions: {str(e)}"
