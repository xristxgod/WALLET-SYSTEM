import typing
from src.models import TokenModel

class Helper:

    @staticmethod
    def get_all_tokens(tokens: typing.List[TokenModel]) -> typing.List[str]:
        return [f"{token.network}|{token.token}" for token in tokens]
