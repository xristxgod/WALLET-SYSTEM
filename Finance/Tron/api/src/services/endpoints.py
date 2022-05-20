from typing import Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from src.services.wallet import wallet
from src.services.transactions import transaction_parser
from src.services.schemas import (
    ResponseCreateWallet, BodyCreateWallet,
    BodyCreateTransaction, BodySignAndSendTransaction,
    ResponseGetOptimalFee, ResponseSignAndSendTransaction,
    ResponseAllTransaction, ResponseGetBalance,
    ResponseCreateTransaction
)
from src.types import TAddress, TransactionHash, Coins
from config import logger

router = APIRouter(prefix="/api")

# <<<----------------------------------->>> Wallet Info <<<---------------------------------------------------------->>>

@router.post(
    "/tron/create/wallet", response_model=ResponseCreateWallet,
    description="This method creates a tron wallet", tags=["WALLET"]
)
async def create_wallet(body: BodyCreateWallet, network: Optional[str] = "tron"):
    try:
        logger.error(f"Calling '/{network}/create/wallet'")
        if Coins.is_native(coin=network) or Coins.is_token(coin=network):
            return wallet.create_wallet(body=body)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Network "{network}" was not found')
    except Exception as error:
        return {"error": str(error)}

@router.get(
    "/{network}/balance/{address}", description="Show balance on wallet address native/token",
    response_model=ResponseGetBalance, tags=["WALLET"]
)
async def get_balance(address: TAddress, network: Optional[str] = "tron"):
    try:
        logger.error(f"Calling '{network}/balance/{address}'")
        if Coins.is_native(coin=network):
            return await wallet.get_balance(address=address)
        elif Coins.is_token(coin=network):
            return await wallet.get_balance(address=address, token=Coins.is_token(coin=network))
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Coin "{network}" was not found')
    except Exception as error:
        return JSONResponse(content={"error": str(error)})

# <<<----------------------------------->>> Fee <<<------------------------------------------------------------------>>>

@router.get(
    "/{network}/fee/{fromAddress}&{toAddress}", description="Get a fixed transaction fee USDT",
    response_model=ResponseGetOptimalFee, tags=["TRANSACTION"]
)
async def get_optimal_fee(fromAddress: TAddress, toAddress: TAddress, network: Optional[str] = "tron"):
    try:
        logger.error(f"Calling '/{network}/fee/{fromAddress}&{toAddress}'")
        if Coins.is_native(coin=network):
            return await wallet.get_optimal_fee(from_address=fromAddress, to_address=toAddress, token="TRX")
        elif Coins.is_token(coin=network):
            return await wallet.get_optimal_fee(
                from_address=fromAddress, to_address=toAddress, token=Coins.is_token(coin=network)
            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Coin "{network}" was not found')
    except Exception as error:
        return JSONResponse(content={"error": str(error)})

# <<<----------------------------------->>> Transaction Info <<<----------------------------------------------------->>>

@router.get(
    "/{network}/transaction/{trxHash}", description="Get transaction by transaction hash",
    response_model=ResponseSignAndSendTransaction, tags=["TRANSACTION"]
)
async def get_transaction_by_tx_id(trxHash: TransactionHash, network: Optional[str] = "tron"):
    try:
        logger.error(f"Calling '/{network}/get-transaction-info/{trxHash}'")
        if Coins.is_native(coin=network) or Coins.is_token(coin=network):
            return ResponseSignAndSendTransaction(
                **((await transaction_parser.get_transaction(transaction_hash=trxHash))[0])
            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Network "{network}" was not found')
    except Exception as error:
        return JSONResponse(content={"error": str(error)})

@router.get(
    "/{network}/transactions/{address}", description="Get transaction by transaction hash",
    response_model=ResponseAllTransaction, tags=["TRANSACTION"]
)
async def get_all_transactions_by_address(address: TAddress, network: str):
    try:
        logger.error(f"Calling '/{network}/get-all-transactions/{address}'")
        if Coins.is_token(coin=network) or Coins.is_native(coin=network):
            return await transaction_parser.get_all_transactions(
                    address=address,
                    token=Coins.is_token(coin=network) if not Coins.is_native(coin=network) else None
                )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Network "{network}" was not found')
    except Exception as error:
        return JSONResponse(content={"error": str(error)})

# <<<----------------------------------->>> Create transaction <<<--------------------------------------------------->>>

@router.post(
    "/{network}/create/transaction", response_model=ResponseCreateTransaction,
    tags=["TRANSACTION"], description="Create transaction with sending from any address to any another",
)
async def create_transaction(body: BodyCreateTransaction, network: Optional[str] = "tron"):
    try:
        logger.error(f"Calling '/{network}/create-transaction'")
        if Coins.is_native(coin=network):
            return await wallet.create_transaction(body=body, token="TRX")
        elif Coins.is_token(coin=network):
            return await wallet.create_transaction(body=body, token=Coins.is_token(coin=network))
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Coin "{network}" was not found')
    except Exception as error:
        return JSONResponse(content={"error": str(error)})

# <<<----------------------------------->>> Sing and Send transactions <<<------------------------------------------->>>

@router.post(
    "/{network}/send/transaction", description="Sign and Send a transaction",
    response_model=ResponseSignAndSendTransaction, tags=["TRANSACTION"]
)
async def sign_and_send_transaction(body: BodySignAndSendTransaction, network: str):
    try:
        logger.error(f"Calling '/{network}/sign-send-transaction'")
        if Coins.is_token(coin=network) or Coins.is_native(coin=network):
            return await wallet.sign_and_send_transaction(body=body)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Coin "{network}" was not found')
    except Exception as error:
        return JSONResponse(content={"error": str(error)})
