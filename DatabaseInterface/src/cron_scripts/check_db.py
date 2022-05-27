import asyncio
from typing import Dict

from src.cron_scripts import DB
from api.utils.utils import Utils
from api.services.__init__ import transaction_repository
from config import logger

async def __check_cache(chat_id: int, networks: Dict) -> bool:
    for network, transaction in networks.items():
        if not Utils.is_have_time(transaction.get("timestamp"), 30, 30):
            logger.info(f"[DEL] Transaction | ChatID: {chat_id} | Network: {network}")
            transaction_repository.remove_transaction(chat_id=chat_id, network=network)
    return True

async def check_transaction_repository_cache():
    await asyncio.gather(*[
        __check_cache(chat_id=chat_id, networks=networks)
        for chat_id, networks in transaction_repository.transactions.items()
    ])

async def __check_db(transaction_info: Dict) -> bool:
    if transaction_info.get("status") == 0 and Utils.is_have_time(transaction_info.get("time"), 30, 30):
        return True
    elif transaction_info.get("status") == 1 and Utils.is_have_time(transaction_info.get("time"), 60, 60):
        return True
    return await DB.delete_transaction(
        user_id=transaction_info.get("user_id"),
        transaction_hash=transaction_info.get("transaction_hash"),
        status=transaction_info.get("status"),
    )

async def check_transaction_model():
    transactions = await DB.get_all_transactions_time(status=(0, 1))
    await asyncio.gather(*[
        __check_db(transaction_info=transaction_info)
        for transaction_info in await DB.get_all_transactions_time(status=(0, 1))
    ])

async def main():
    await asyncio.gather(
        check_transaction_model(),
        check_transaction_repository_cache()
    )
    return True

def run():
    loop = None
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(main())
        loop.close()
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return False
    finally:
        if loop is not None and not loop.is_closed():
            loop.close()

if __name__ == '__main__':
    logger.info("START CRON SCRIPT: CHECKER")
    run()
    logger.info("END CRON SCRIPT: CHECKER")