import json

import art
from src.service import main

if __name__ == '__main__':
    # add/del/upg/get manually to the database.
    art.tprint("ADD/DEL/UPG/GET TO DB", font="")
    print((
        "Which table to manipulate?\n"
        "   1. UserModel - Contains information about users.\n"
        "   2. WalletModel - Contains information about user wallets.\n"
        "   3. WalletTransactionModel - Contains information about transactions on users' wallets.\n"
        "   4. TokenModel - Tokens in the system"
    ))
    table = int(input("Enter the number:      "))
    print((
        "\nWhat method should I use?\n"
        "   1. GET\n"
        "   2. ADD\n"
        "   3. UPG\n"
        "   4. DEL"
    ))
    method = int(input("Enter the number:      "))
    if method in [1, 4]:
        print((
            "Enter the id of the field you want to do this with:"
            "   To get or delete all of them, type `ADD`!"
        ))
        _id = input("Enter the id number:      ")
        print("\nProcessing...")
        if not _id.isdigit() and _id.lower() == "add":
            status = main(table=table, method=method, is_all=True)
        else:
            status =main(table=table, method=method, _id=int(_id))
    elif method == 2:
        print((
            "Enter the data you want to add in `JSON` format:\n"
            'Example for the UserModel table: {"id": yourChatId, "username": yourTelegramName, "is_admin": TrueOrFalse}'
        ))
        data = json.dumps(input("Enter:"))
        print("\nProcessing...")
        status =main(table=table, method=2, data=data)
    elif method == 3:
        print((
            "Enter the id of the user you want to change the data from:\n"
        ))
        _id = input("Enter the id number:      ")
        print((
            "Enter the data you want to change in JSON format:\n"
            'Example for the UserModel table: {"username": nameByUpgrade, "is_admin": TrueOrFalse}'
        ))
        data = json.dumps(input("Enter:"))
        print("\nProcessing...")
        status = main(table=table, method=3, data=data, _id=_id)
    else:
        raise Exception()
    print(status)

