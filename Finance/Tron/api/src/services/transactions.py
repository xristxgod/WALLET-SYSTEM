import asyncio
import random
import typing
from decimal import Decimal
from typing import List, Dict, Union

import requests

from src.services.schemas import ResponseSignAndSendTransaction, ResponseAllTransaction
from src.__init__ import DB
from src.services import NodeTron
from src.types import TAddress, TransactionHash, Coins
from config import Config, decimals

def get_all_trx_for_format(txns: List, address: TAddress):
    res = []
    for txn in txns:
        res.append(ResponseSignAndSendTransaction(**txn))
    return ResponseAllTransaction(
        address=address,
        data=res
    )

class TransactionParser(NodeTron):

    async def get_transaction(self, transaction_hash: TransactionHash) -> typing.List:
        return await self.__get_transactions(transactions=[await self.node.get_transaction(txn_id=transaction_hash)])

    @staticmethod
    async def get_url(network: str, address: TAddress, token: str) -> str:
        url = f"https://api.{'' if network == 'mainnet' else f'{network.lower()}.'}trongrid.io/v1/accounts/{address}/transactions"
        url += f"/trc20?limit=200&contract_address={(await DB.get_token_info(token=token))['address']}" if token is not None else "?limit=200"
        return url

    @staticmethod
    def get_headers():
        return {"Accept": "application/json", "TRON-PRO-API-KEY": Config.TRON_API_KEYS[random.randint(0, 2)]}

    async def get_all_transactions(self, address: TAddress, token: str = None) -> ResponseAllTransaction:
        transactions = requests.get(
            (await TransactionParser.get_url(network=NodeTron.NETWORK, address=address, token=token)),
            headers=TransactionParser.get_headers()
        ).json()["data"]
        return get_all_trx_for_format(
            txns=await self.__get_transactions(transactions=transactions, token=token),
            address=address
        )

    async def __get_transactions(self, transactions: List, token: str = None) -> List:
        """Get all transactions by address"""
        fund_trx_for_send = []
        list_transactions = await asyncio.gather(*[
            self.__processing_transactions(
                transactions=transactions[right_border: (right_border + 1)],
                token=token if token else None
            )
            for right_border in range(len(transactions))
        ])
        await self.node.close()
        for transactions in list_transactions:
            fund_trx_for_send.extend(transactions)
        return fund_trx_for_send

    async def __processing_transactions(self, transactions: Dict, token: str = None) -> List:
        """
        Unpacking transactions and checking for the presence of required addresses in them
        :param transactions: Set of transactions
        """
        funded_trx_for_sending = []
        for txn in transactions:
            if token:
                funded_trx_for_sending.append(await self.__packaging_for_dispatch_token(txn=txn))
            else:
                txn_type = txn["raw_data"]["contract"][0]["type"]
                funded_trx_for_sending.append(await self.__packaging_for_dispatch(txn=txn, txn_type=txn_type))
        return funded_trx_for_sending

    async def __packaging_for_dispatch_token(self, txn: Dict) -> Union[Dict, None]:
        """
        Packaging the necessary transaction to send
        :param txn: Transaction
        :param txn_type: Transaction type
        """
        if not Coins.is_token(txn["token_info"]["symbol"]):
            return None
        tx_fee = await self.node.get_transaction_info(txn_id=txn["transaction_id"])
        if "fee" in tx_fee:
            fee = "%.8f" % decimals.create_decimal(self.fromSun(tx_fee["fee"]))
        else:
            fee = 0
        amount = "%.8f" % decimals.create_decimal(int(txn["value"]) / (10 ** int(txn["token_info"]["decimals"])))
        return {
            "time": txn["block_timestamp"],
            "transactionHash": txn["transaction_id"],
            "fee": fee,
            "amount": amount,
            "senders": [
                {
                    "address": txn["from"],
                    "amount": amount
                }
            ],
            "recipients": [
                {
                    "address": txn["to"],
                    "amount": amount
                }
            ],
            "token": txn["token_info"]["symbol"]
        }

    async def __packaging_for_dispatch(self, txn: Dict, txn_type: str) -> Dict:
        """
        Packaging the necessary transaction to send
        :param txn: Transaction
        :param txn_type: Transaction type
        """
        try:
            txn_values = txn["raw_data"]["contract"][0]['parameter']["value"]
            try:
                fee_limit = await self.node.get_transaction_info(txn["txID"])
                if "fee" not in fee_limit:
                    raise Exception
                fee = "%.8f" % decimals.create_decimal(self.fromSun(fee_limit["fee"]))
            except Exception:
                fee = 0
            values = {
                "time": txn["raw_data"]["timestamp"] if "timestamp" in txn["raw_data"] else "",
                "transactionHash": txn["txID"],
                "transactionType": txn_type,
                "fee": fee,
                "amount": 0,
                "senders": [
                    {
                        "address": self.node.to_base58check_address(txn_values["owner_address"])
                    }
                ],
                "recipients": []
            }
            # TRX or TRC10
            if txn_type in ["TransferContract", "TransferAssetContract"]:
                amount = "%.8f" % decimals.create_decimal(self.fromSun(txn_values["amount"]))
                values["amount"] = amount
                values["recipients"] = [{
                    "address": self.node.to_base58check_address(txn_values["to_address"]),
                    "amount": amount
                }]
                values["senders"][0]["amount"] = amount
                if "asset_name" in txn_values:
                    values["token"] = self.node.get_asset(id=txn_values["asset_name"])
            # TRC20
            elif txn_type == "TriggerSmartContract":
                smart_contract = await self.__smart_contract_transaction(
                    data=txn_values["data"], contract_address=txn_values["contract_address"]
                )
                if "data" in smart_contract:
                    values["data"] = smart_contract["data"]
                else:
                    amount = smart_contract["amount"]
                    values["senders"][0]["amount"] = amount
                    values["recipients"] = [{
                        "address": smart_contract["to_address"],
                        "amount": amount
                    }]
                    values["token"] = smart_contract["token"]
                    values["amount"] = amount
            # Freeze or Unfreeze balance
            elif txn_type in ["FreezeBalanceContract", "UnfreezeBalanceContract"]:
                if "resource" in txn_values:
                    values["resource"] = txn_values["resource"]
                else:
                    values["resource"] = "BANDWIDTH"

                if "receiver_address" in txn_values:
                    values["recipients"] = [{
                        "address": self.node.to_base58check_address(txn_values["receiver_address"]),
                        "amount": 0
                    }]
                else:
                    values["recipients"] = [{
                        "address": values["senders"][0]["address"],
                        "amount": 0
                    }]

                if "frozen_balance" in txn_values:
                    amount = str(self.fromSun(txn_values["frozen_balance"]))
                    values["amount"] = amount
                    values["senders"][0]["amount"] = amount
                    values["recipients"][0]["address"] = amount
            # Vote
            elif txn_type == "VoteWitnessContract":
                try:
                    values["recipients"] = [{
                        "address": txn_values["votes"][0]["vote_address"],
                        "voteCount": txn_values["votes"][0]["vote_count"]
                    }]
                except Exception as error:
                    pass
            return values
        except Exception as error:
            return {}

    async def __smart_contract_transaction(self, data: str, contract_address: TAddress) -> Dict:
        """
        Unpacking a smart contract
        :param data: Smart Contract Information
        :param contract_address: Smart contract (Token TRC20) address
        """
        try:
            contract = await self.node.get_contract(addr=contract_address)
            token_name = await contract.functions.symbol()
            dec = await contract.functions.decimals()
            amount = Decimal(value=int("0x" + data[72:], 0) / 10 ** int(dec))
            to_address = self.node.to_base58check_address("41" + data[32:72])
            return {
                "to_address": to_address,
                "token": token_name,
                "amount": "%.8f" % amount
            }
        except Exception as error:
            return {"data": str(data)}

transaction_parser = TransactionParser()

if __name__ == '__main__':
    address = "YourAddress"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(transaction_parser.get_all_transactions(address))
    print(result)