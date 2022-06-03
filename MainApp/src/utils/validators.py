from typing import Optional, List, Dict

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from src.utils.utils import Utils
from src.utils.types import CRYPTO_NETWORK, CRYPTO_ADDRESS, CRYPTO_MNEMONIC


class ImageValidators:
    """Image validators"""
    @staticmethod
    def validate_logo(logo) -> Optional:
        width, height = get_image_dimensions(logo)
        if width > 300 or width < 100:
            raise ValidationError("The image is %i pixel wide. It's supposed to be 200px" % width)
        elif height > 300 or height < 100:
            raise ValidationError("The image is %i pixel high. It's supposed to be 200px" % height)

    @staticmethod
    def validate_image_expansion(image) -> Optional:
        _, extension = str(image).split(".")
        if extension not in ["png", "ico", "jpeg"]:
            raise ValidationError("The extension of the image: {} and should be {}.".format(
                extension, ["png", "ico", "jpeg"]
            ))


class WalletValidators:
    """Wallet validators"""
    LEN_MNEMONIC = [3, 6, 9, 12, 15, 18, 21, 24]

    @staticmethod
    def validate_mnemonic(mnemonic: CRYPTO_MNEMONIC) -> Optional:
        if len(mnemonic.split(" ")) not in WalletValidators.LEN_MNEMONIC:
            raise ValidationError("The mnemonic phrase should consist of {} words, and you have only: {}.".format(
                WalletValidators.LEN_MNEMONIC, len(mnemonic.split(" "))
            ))
        if len(mnemonic.split(" ")) != len(set(mnemonic.split(" "))):
            raise ValidationError("The mnemonic phrase has duplicate meanings!")


class TransactionValidators:
    """Transaction validators"""
    @staticmethod
    def validate_participants(participants: List[Dict[CRYPTO_ADDRESS, float]]):
        if participants != {}:
            for participant in participants:
                if participant.keys() not in ["address", "amount"]:
                    raise ValidationError((
                        "This type of data is not suitable. The list should consist of dictionaries. "
                        "Example: [{'address': wallet_address, 'amount': 12.3312}]"
                    ))
                if not Utils.is_number(participant.get("amount")):
                    raise ValidationError("The amount value must be a number!")
