from src.parser.__init__ import JSONMessage

class JSONError(JSONMessage):
    def __init__(self, error: Exception, func: str, chat_id: int, **kwargs):
        super().__init__(**kwargs)
        self.chat_id: int = chat_id
        self.func: str = func
        self.error: Exception = error

    @property
    def generate_text(self) -> str:
        pass

class JSONTransaction(JSONMessage):

    def __init__(self):
        pass