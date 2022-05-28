from src.parser.__init__ import Message
from src.utils.types import CoinsURL, Symbol, FullNetwork, TGChatID
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
        self.url: str = Utils.get_blockchain_url(network=self.network, transaction_hash=transaction_hash)
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

    def __init__(self, text: str, **kwargs):
        super(Message, self).__init__(**kwargs)
        self.text = text

    def generate_text(self, status: str = "GOOD"):
        return (
            f"{self.__dict__.get(status)}"
            f"{self.text}"
        )

class MessageUser(Message):
    REG_ADMIN = f"{Symbol.ADMIN} New admin!\n"
    REG_USER = f"{Symbol.REG} New user!\n"
    ADD = f"{Symbol.ADD} There was a replenishment: <amount> <network>\n"
    DEC = f"{Symbol.DEC} Funds were debited: <amount> <network>\n"
    INFO = f"{Symbol.INFO} Urgent information!\n"

    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)
        self.chat_id: TGChatID = kwargs.get("chat_id")
        self.username: str = kwargs.get("username")
        self.amount: float = kwargs.get("amount")
        self.network: FullNetwork = kwargs.get("network")
        self.url: str = Utils.get_blockchain_url(
            self.network.split("-")[0], transaction_hash=kwargs.get("transaction_hash")
        )
        self.text: str = kwargs.get("text")

    def generate_text(self, status: str):
        text = f"{self.__dict__.get(status)}"
        if status in ["ADD", "DEC"]:
            return (
                f"{text}"
                f"ChatID: {self.chat_id}\n"
                f"Username: {self.username}"
                f"<b><a href='{self.url}'>Check transaction:</a></b>\n"
            )
        elif status == "REG":
            return (
                f"{text}"
                f"ChatID: {self.chat_id}\n"
                f"Username: {self.username}"
            )
        else:
            return (
                f"{text}"
                f"{self.text}"
            )