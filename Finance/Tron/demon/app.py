from src.demon import TransactionDemon
from src.search_by_addresses import AddressesDemon
from config import Config, logger
from asyncio import run

if __name__ == '__main__':
    logger.error(f"DEMON IS STARTING. NETWORK: {Config.NODE_NETWORK}")
    run(TransactionDemon().start())