import json

import requests
from decouple import config

from constants.currencies import MAPPER


class WiseService:
    def __init__(self):
        self.token = config("WISE_KEY")
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        self.main_url = config("WISE_URL")
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self):
        url = f"{self.main_url}/v1/profiles"
        resp = requests.get(url, headers=self.headers)
        data = resp.json()
        profile_id = [o["id"] for o in data if o["type"] == "personal"][0]
        return profile_id

    def create_quote(self, source_currency, target_currency, amount):
        url = f"{self.main_url}/v2/quotes"
        data = {
            "sourceCurrency": source_currency,
            "targetCurrency": target_currency,
            "targetAmount": amount,
            "profile": self.profile_id
        }
        # data=json.dumps(data) is the same
        resp = requests.post(url, json=data, headers=self.headers)
        return resp.json()["id"]

    def create_recipient(self, full_name, iban, country):
        url = f"{self.main_url}/v1/accounts"
        data = {
            "currency": MAPPER[country]["currency"],
            "type": MAPPER[country]["type"],
            "profile": self.profile_id,
            "accountHolderName": full_name,
            "legalType": "PRIVATE",
            "details": {
                "iban": iban,
            }
        }
        resp = requests.post(url, data=json.dumps(data), headers=self.headers)
        return resp.json()["id"]

    def create_transfer(self, recipient_account_id, quote_id, customer_transaction_id):
        url = f"{self.main_url}/v1/transfers"
        data = {
            "targetAccount": recipient_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id
        }
        resp = requests.post(url, json=data, headers=self.headers)
        return resp.json()

    def fund_transfer(self, transfer_id):
        url = f"{self.main_url}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"
        data = {
            "type": "BALANCE"
        }
        resp = requests.post(url, json=data, headers=self.headers)
        return resp.json()

    def cancel_transfer(self, transfer_id):
        url = f"{self.main_url}/v1/transfers/{transfer_id}/cancel"
        resp = requests.put(url, headers=self.headers)
        return resp.json()

# if __name__ == "__main__":
#     wise = WiseService()


# BG89370400440532013000, DE89370400440532013000

# print(wise.profile_id)
# print(wise.create_quote("EUR", "EUR", 20))
# print(wise.create_recipient("Koki Kokov", "DE89370400440532013000", "DE"))

# quote_id = wise.create_quote("EUR", "EUR", 20)
# recipient_id = wise.create_recipient("Koki Kokov", "DE89370400440532013000", "DE")
# customer_transaction_id = str(uuid.uuid4())
# transfer_id = wise.create_transfer(recipient_id, quote_id, customer_transaction_id)["id"]
# fund_transfer = wise.fund_transfer(transfer_id)
