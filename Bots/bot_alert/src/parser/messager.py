from src.parser.__init__ import Message
from src.utils.types import CoinsURL, Symbol, FullNetwork
from src.utils.utils import Utils

class MessageTransaction(Message):
    """Transaction message"""
    PROCESSING = f"{Symbol.DEC} The transaction on <b><network></b> network has been created!\n"
    CREATE = f"{Symbol.ADD} The transaction on <b><network></b> network is waiting to be sent!\n"
    SENT = f"{Symbol.ADD} The transaction on <b><network></b> network has been sent!\n"
    ERROR = f"{Symbol.DEC} The transaction on <b><network></b> network is ERROR!\n"

    def __init__(self, network: FullNetwork, transaction_hash: str, amount: float, fee: float, **data):
        super(Message, self).__init__(**data)
        self.network, self.token = network.split("-")
        self.url: str = CoinsURL.get_blockchain_url_by_network(self.network) + f"/#/transaction/{transaction_hash}"
        self.inputs, self.outputs = Utils.get_correct_tx_data(
            inputs=data.get("inputs"),
            outputs=data.get("outputs"),
            network=self.network
        )
        self.amount: str = f"{amount} {self.network}-{self.token}"
        self.fee: str = f"{fee} {CoinsURL.get_native_by_network(self.network)}"

    def generate_text(self, status: str = "PROCESSING") -> str:
        return (
            f"{self.__dict__.get(status).replace('<network>', self.network)}"
            f"The Sender/s:\n{self.inputs}"
            f"The Recipient/s:\n{self.outputs}"
            f"Transaction amount: <b>{self.amount}</b>\n"
            f"Commission: <b>{self.fee}</b>\n"
            f"                                          <b><a href='{self.url}'>Check transaction:</a></b>\n"
        )

class MessageChecker(Message):
    GOOD = f"{Symbol.ADD} Good news:\n"
    BAD = f"{Symbol.DEC} Bad news:\n"
    INFO = f"{Symbol.ADD} Info:\n"

    def __init__(self, text: str, **data):
        super(Message, self).__init__(**data)
        self.text = text

    def generate_text(self, status: str = "GOOD"):
        return (
            f"{MessageChecker.__dict__.get(status)}"
            f"{self.text}"
        )