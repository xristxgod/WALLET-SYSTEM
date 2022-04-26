import typing

class Events:
    """
    def main():
        dispatch("event_name", arg=1, arg2="12")
    register_handler("event_name", func_name)
    register_handler("event_name", func_name_two)
    """
    def __init__(self):
        self.event_handler = {}

    def register_handler(self, event: str, func: typing.Callable):
        functions = self.event_handler.get(event)
        if functions is None:
            self.event_handler[event] = [func]
        else:
            functions.append(func)

    def dispatch(self, event: str, **kwargs):
        functions = self.event_handler.get(event)

        if functions is None:
            raise ValueError(f"Unknown event: {event}")

        for func in functions:
            func(**kwargs)