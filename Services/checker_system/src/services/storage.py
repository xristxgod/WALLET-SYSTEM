from datetime import datetime
import asyncio

lock = asyncio.Lock()

class Storage:
    def __init__(self):
        self.__data = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(cls.__class__, cls).__new__(cls)
        return cls.instance

    async def add_error(self, title: str):
        self.__data.update({title: datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    async def remove_error(self, title: str):
        if title in self.__data.keys():
            del self.__data[title]

    async def get_text(self):
        data = self.__data.copy()
        return '\n'.join([f'🔴 {x}: {y}' for x, y in data.items()])

storage = Storage()