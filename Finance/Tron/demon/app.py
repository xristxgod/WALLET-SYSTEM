import asyncio

from src.demon import TransactionDemon
from config import Config, logger

if __name__ == '__main__':
    logger.error(f"DEMON IS STARTING. NETWORK: {Config.NETWORK}")
    loop = None
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(TransactionDemon().start())
    except Exception as error:
        logger.error(f"ERROR: {error}")
    finally:
        if loop is not None and not loop.is_closed():
            loop.close()