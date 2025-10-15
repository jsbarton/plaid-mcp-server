# Plaid API client wrapper
import os
from dotenv import load_dotenv
from plaid.api.plaid_api import PlaidApi
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)

load_dotenv()

client_id = os.getenv("PLAID_CLIENT_ID")
secret = os.getenv("PLAID_SECRET")

configuration = Configuration(
    host="https://sandbox.plaid.com",
    api_key={
        "clientId": client_id,
        "secret": secret,
    },
)

api_client = ApiClient(configuration)
client = PlaidApi(api_client)


def get_access_token(public_token: str) -> str:
    try:
        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response["access_token"]
    except Exception as e:
        # generate a new hosted link here
        return "public token expired"

    return access_token
