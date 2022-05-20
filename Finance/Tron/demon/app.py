from src.demon import TransactionDemon
from config import Config, logger
from asyncio import run

if __name__ == '__main__':
    logger.error(f"DEMON IS STARTING. NETWORK: {Config.NETWORK}")
    run(TransactionDemon().start(
        start_block=24578584,
        end_block=24578586
    ))
