# IMPORTS

# external
from typing import List
from base64 import b64encode

# local
from .manager import Manager
from .manager_config import MANAGER_CONFIGS
from .market import Market
from .market_config import MARKET_CONFIGS
from .lending_config import MANAGER_STRINGS

# INTERFACE

class LendingClient:
    def __init__(self, algofi_client):
        """Constructor for the client used to interact with algofi lending protocol

        :param algofi_client: Client for the algofi protocols
        :type algofi_client: :class:`AlgofiClient`
        """

        self.algofi_client = algofi_client
        self.algod = algofi_client.algod
        self.indexer = algofi_client.indexer
        self.historical_indexer = algofi_client.historical_indexer
        
        self.manager_config = MANAGER_CONFIGS[self.algofi_client.network]
        self.market_configs = MARKET_CONFIGS[self.algofi_client.network]
        
        self.manager = Manager(self, self.manager_config)
        self.markets = {}
        for market_config in self.market_configs:
            self.markets[market_config.app_id] = Market(self, market_config)

    def get_storage_accounts(self, verbose=False):
        """Fetches the list of user storage accounts on the lending protocol from the blockchain

        :param verbose: return account address with full account data (e.g. created apps / assets, local state, balances)
        :type verbose: bool, optional
        :return: list of storage account address strings
        :rtype: list
        """

        next_page = ""
        accounts = []
        while next_page is not None:
            account_data = self.indexer.accounts(limit=1000, next_page=next_page, application_id=self.manager.app_id, exclude="assets")
            accounts_filtered = []
            for account in account_data["accounts"]:
                user_local_state = account.get("apps-local-state",[])
                for app_local_state in user_local_state:
                    if app_local_state["id"] == self.manager.app_id:
                        fields = app_local_state.get("key-value", [])
                        for field in fields:
                            key = field.get("key", None)
                            if key ==  b64encode(bytes(MANAGER_STRINGS.user_account, "utf-8")).decode("utf-8"):
                                accounts_filtered.append(account)
            accounts.extend([(account if verbose else account["address"]) for account in accounts_filtered])
            if "next-token" in account_data:
                next_page = account_data["next-token"]
            else:
                next_page = None
        return accounts
