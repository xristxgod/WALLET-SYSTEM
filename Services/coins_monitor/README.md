Coinser bot
======

> This bot collects information (price, rate) about certain currencies and puts them in the database.

Start in manual mode:
```shell
# Run in an infinite loop:
python3 ./Services/coins_monitor/app.py 
# Run downloading the top 100 coins.
python3 ./Services/coins_monitor/download_top_100_coins.py
# Write data about a certain period to the database.
python3 ./Services/coins_monitor/go_to_deep_history.py --start timestampFormat --end timestampFormat
python3 ./Services/coins_monitor/go_to_deep_history.py -s timestampFormat -e timestampFormat
```