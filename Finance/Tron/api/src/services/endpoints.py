from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from src.auth.auth_handler import JWTBearer
from src.services.wallet import wallet
from src.services.transactions import get_transaction_by_tx_hash, get_transactions_by_address
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
    description="This method creates a tron wallet", tags=["WALLET"],
    dependencies=[Depends(JWTBearer())],
)
async def create_wallet(body: BodyCreateWallet):
    try:
        logger.info(f"Calling 'api/tron/create/wallet'")
        return wallet.create_wallet(body=body)
    except Exception as error:
        return {"error": str(error)}

@router.get(
    "/{network}/balance/{address}", description="Show balance on wallet address native/token",
    response_model=ResponseGetBalance, tags=["WALLET"], dependencies=[Depends(JWTBearer())]
)
async def get_balance(address: TAddress, network: Optional[str] = "tron"):
    try:
        logger.info(f"Calling 'api/{network}/balance/{address}'")
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
    response_model=ResponseGetOptimalFee, tags=["TRANSACTION"], dependencies=[Depends(JWTBearer())]
)
async def get_optimal_fee(fromAddress: TAddress, toAddress: TAddress, network: Optional[str] = "tron"):
    try:
        logger.info(f"Calling 'api/{network}/fee/{fromAddress}&{toAddress}'")
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
    "/tron/transaction/{tx_hash}", description="Get transaction by transaction hash",
    response_model=ResponseSignAndSendTransaction, tags=["TRANSACTION"]
)
async def get_transaction_by_tx_id(tx_hash: TransactionHash):
    try:
        logger.info(f"Calling 'api/tron/transaction/{tx_hash}'")
        return await get_transaction_by_tx_hash(tx_hash=tx_hash)
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return JSONResponse(content={})

@router.get(
    "/{network}/transactions/{address}", description="Get transaction by transaction hash",
    response_model=ResponseAllTransaction, tags=["TRANSACTION"]
)
async def get_all_transactions_by_address(address: TAddress, network: str):
    try:
        logger.info(f"Calling 'api/{network}/transactions/{address}'")
        if Coins.is_token(coin=network) or Coins.is_native(coin=network):
            return await get_transactions_by_address(
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
    dependencies=[Depends(JWTBearer())]
)
async def create_transaction(body: BodyCreateTransaction, network: Optional[str] = "tron"):
    try:
        logger.info(f"Calling 'api/{network}/create/transaction'")
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
    response_model=ResponseSignAndSendTransaction, tags=["TRANSACTION"],
    dependencies=[Depends(JWTBearer())]
)
async def sign_and_send_transaction(body: BodySignAndSendTransaction, network: str):
    try:
        logger.info(f"Calling 'api/{network}/send/transaction'")
        if Coins.is_token(coin=network) or Coins.is_native(coin=network):
            return await wallet.sign_and_send_transaction(body=body)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Coin "{network}" was not found')
    except Exception as error:
        return JSONResponse(content={"error": str(error)})