import asyncio
import random
import typing
from decimal import Decimal
from typing import Optional, Union, List, Dict

import requests
from tronpy.async_tron import AsyncTron, AsyncHTTPProvider

from src.services.schemas import BodyInputsOrOutputs, ResponseSignAndSendTransaction, ResponseAllTransaction
from src.__init__ import DB
from src.services import NodeTron
from src.utils import TronUtils
from src.types import TAddress, TransactionHash, Coins
from config import Config, decimals

def get_all_trx_for_format(txns: List, address: TAddress):
    res = []
    for txn in txns:
        res.append(txn)
    return ResponseAllTransaction(
        address=address,
        transactions=res
    )

class TransactionParser:
    # Provider config
    PROVIDER = AsyncHTTPProvider(Config.NODE_URL)
    NETWORK: str = "shasta" if Config.NETWORK == "TESTNET" else "mainnet"
    # Converts
    fromSun = staticmethod(TronUtils.from_sun)
    toSun = staticmethod(TronUtils.to_sun)

    def __init__(self):
        """
        Connect to Tron Node
        :param node_url: Node url
        :param network: Network | mainnet or shasta
        """
        self.node = AsyncTron(
            provider=NodeTron.PROVIDER if NodeTron.NETWORK == "mainnet" else None,
            network=NodeTron.NETWORK
        )

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

    async def __packaging_for_dispatch_token(self, txn: Dict) -> Optional[ResponseSignAndSendTransaction]:
        """
        Packaging the necessary transaction to send
        :param txn: Transaction
        :param txn_type: Transaction type
        """
        if not Coins.is_token(txn["token_info"]["symbol"]):
            return None
        tx_fee = await self.node.get_transaction_info(txn_id=txn["transaction_id"])
        if "fee" in tx_fee:
            fee = decimals.create_decimal(self.fromSun(tx_fee["fee"]))
        else:
            fee = decimals.create_decimal(0)
        amount = decimals.create_decimal(int(txn["value"]) / (10 ** int(txn["token_info"]["decimals"])))
        return ResponseSignAndSendTransaction(
            time=txn["block_timestamp"],
            transactionHash=txn["transaction_id"],
            fee=fee,
            amount=amount,
            inputs=[BodyInputsOrOutputs(address=txn["from"], amount=amount)],
            outputs=[BodyInputsOrOutputs(address=txn["to"], amount=amount)],
            token=txn["token_info"]["symbol"]
        )

    async def __packaging_for_dispatch(self, txn: Dict, txn_type: str) -> Union[ResponseSignAndSendTransaction, Dict]:
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
                fee = decimals.create_decimal(self.fromSun(fee_limit["fee"]))
            except Exception:
                fee = decimals.create_decimal(0)
            values = ResponseSignAndSendTransaction(
                time=txn["raw_data"]["timestamp"] if "timestamp" in txn["raw_data"] else 0,
                transactionHash=txn["txID"],
                fee=fee,
                amount=decimals.create_decimal(0),
                inputs=[
                    BodyInputsOrOutputs(
                        address=self.node.to_base58check_address(txn_values["owner_address"]),
                        amount=decimals.create_decimal(0)
                    )
                ],
                outputs=[],
            )
            # TRX or TRC10
            if txn_type in ["TransferContract", "TransferAssetContract"]:
                amount = decimals.create_decimal(self.fromSun(txn_values["amount"]))
                values.amount = amount
                values.outputs = [BodyInputsOrOutputs(
                    address=self.node.to_base58check_address(txn_values["to_address"]),
                    amount=amount
                )]
                values.inputs[0].amount = amount
                if "asset_name" in txn_values:
                    values.token = self.node.get_asset(id=txn_values["asset_name"])
            # TRC20
            elif txn_type == "TriggerSmartContract":
                smart_contract = await self.__smart_contract_transaction(
                    data=txn_values["data"], contract_address=txn_values["contract_address"]
                )
                if "data" in smart_contract:
                    values.data = smart_contract["data"]
                else:
                    amount = decimals.create_decimal(smart_contract["amount"])
                    values.inputs[0].amount = amount
                    values.outputs = [BodyInputsOrOutputs(address=smart_contract["to_address"], amount=amount)]
                    values.token = smart_contract["token"]
                    values.amount = amount
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
                "amount": amount
            }
        except Exception as error:
            return {"data": str(data)}

    async def close_session(self):
        if self.node is not None:
            await self.node.close()

async def get_transaction_by_tx_hash(tx_hash: str) -> ResponseSignAndSendTransaction:
    transaction_parser = None
    try:
        transaction_parser = TransactionParser()
        return (await transaction_parser.get_transaction(transaction_hash=tx_hash))[0]
    finally:
        if transaction_parser is not None:
            await transaction_parser.close_session()

async def get_transactions_by_address(address: TAddress, token: str = None) -> ResponseAllTransaction:
    transaction_parser = None
    try:
        transaction_parser = TransactionParser()
        return await transaction_parser.get_all_transactions(address=address, token=token)
    finally:
        if transaction_parser is not None:
            await transaction_parser.close_session()

if __name__ == '__main__':
    address = "YourAddress"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(get_transactions_by_address(address))
    print(result)