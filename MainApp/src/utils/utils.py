import secrets
import string
import base64
from datetime import datetime, timedelta
from typing import Union, Dict

import pyotp
from django.utils.safestring import mark_safe
from django.db import models


class UtilsImage:
    """Utils for image"""
    @staticmethod
    def image_url(image_url: str = None, method: str = "display"):
        if image_url is None:
            return mark_safe("<img src='' width='{}' />".format(method))

        return mark_safe("<img src='{}' width='{}' />".format(
            image_url, 50 if method == "display" else 200
        ))

    @staticmethod
    def image_name_network(instance: models.Model, filename: str) -> str:
        file_base, extension = filename.split(".")
        return "logo_%s.%s" % (instance.network.lower(), extension)

    @staticmethod
    def image_name_token(instance: models.Model, filename: str) -> str:
        file_base, extension = filename.split(".")
        return "logo_%s.%s" % (f"{instance.network.network.lower()}_{instance.token.lower()}", extension)

    @staticmethod
    def image_transaction_status(instance: models.Model, filename: str) -> str:
        file_base, extension = filename.split(".")
        return "logo_%s.%s" % (f"{instance.id}_{instance.title.lower()}", extension)

    @staticmethod
    def image_name_user(instance: models.Model, filename: str) -> str:
        file_base, extension = filename.split(".")
        return "avatar_%s.%s" % (f"{instance.id}_{instance.username.lower()}", extension)


class Utils:
    """Project utils"""
    @staticmethod
    def is_number(number: Union[float, str, int]) -> bool:
        if isinstance(number, str):
            try:
                if number.find(",") >= 0:
                    number = number.replace(",", ".")
                float(number)
                return True
            except ValueError:
                return False
        else:
            return True

    @staticmethod
    def temporary_password(chat_id: int) -> str:
        return f"temporary_password_{chat_id}"

    @staticmethod
    def is_have_time(timestamp: int, hours: int = 0, minutes: int = 0, seconds: int = 0) -> bool:
        reg_time = datetime.fromtimestamp(timestamp)
        later_time = reg_time + timedelta(minutes=minutes, hours=hours, seconds=seconds)
        now_time = datetime.fromtimestamp(int(datetime.timestamp(datetime.now())))
        return True if reg_time <= now_time <= later_time else False


class UtilsGoogleAuth:
    """Google auth utils"""
    @staticmethod
    def generate_code(length: int = 16):
        secret = "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(length))
        return base64.b32encode(bytearray(secret, 'ascii')).decode('utf-8')[0:16]

    @staticmethod
    def generate_google_auth_code(username: str) -> Dict:
        secret_key = UtilsGoogleAuth.generate_code()
        return {
            "secretKey": secret_key,
            "qrcodeData": pyotp.TOTP(secret_key).provisioning_uri(
                name=f"code@WalletSystem{username.upper()}",
                issuer_name=f"WalletSystem{username.upper()}"
            ),
        }

    @staticmethod
    def is_valid_code(google_auth_code: str, code_now: int) -> bool:
        return pyotp.TOTP(google_auth_code).now() == code_now
