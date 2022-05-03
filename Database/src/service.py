from typing import Dict

from src.settings import db
from src.models import TABLES

class DatabaseRepository:

    @staticmethod
    def get_data(table: int, is_all: bool, _id: int):
        if is_all:
            table: db.Model = TABLES.get(table)
            users = table


    @staticmethod
    def add_new_data(table: int, data: Dict):
        pass

    @staticmethod
    def upgrade_data(table: int, data: Dict, _id: int):
        pass

    @staticmethod
    def delete_data(table: int, is_all: bool, _id: int):
        pass


def main(table: int, method: int, **kwargs):
    if method == 1:
        return DatabaseRepository.get_data(table=table, is_all=kwargs.get("is_all"), _id=kwargs.get("_id"))
    elif method == 2:
        return DatabaseRepository.add_new_data(table=table, data=kwargs.get("data"))
    elif method == 3:
        return DatabaseRepository.upgrade_data(table=table, data=kwargs.get("data"), _id=kwargs.get("_id"))
    else:
        return DatabaseRepository.delete_data(table=table, is_all=kwargs.get("is_all"), _id=kwargs.get("_id"))
