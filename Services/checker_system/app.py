from asyncio import run
from src.checker import Checker


if __name__ == '__main__':
    run(Checker.check_all())