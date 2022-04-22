Sender bot
======

> This bot is used to forward various messages from RabbitMQ to telegram bot (bot_alert)

Start in manual mode:
```shell
# Check for unsent messages. If found, then send it immediately.
python3 ./Services/is_not_send.py --send
python3 ./Services/is_not_send.py -s
# Check for unsent messages. If found, then just output to the terminal.
python3 ./Services/is_not_send.py
python3 ./Services/is_not_send.py
# Run
python3 ./Services/app.py
```