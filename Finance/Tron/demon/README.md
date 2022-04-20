TRON API for Python
===================

Search for Tron positions in a transaction array of addresses.

Usage
=====

Before starting in the `.env` file:

>1. Specify `RabbitMQURL`, this is the path to RabbitMQ via `amqp` or `amqps` protocol. It is necessary to send the verified addresses to the queue.
    >`Example: "amqp://guest:guest@localhost:5672/%2F", "amqp://www-data:rabbit_pwd@rabbit1/web_messages"`
>2. Specify the `Queue` name of the queue to which the already verified data will be sent.
>3. Specify the `DataBaseURL` path to the database, you need to take the address from the database. `Example: "postgresql://postgres:mamedov00@localhost/acc"`
>4. Specify the `TronGridAPIKEY` or `listTronGridAPIKEY` api key or keys for TronGird to connect to the node. You can get it on the website: `https://www.trongrid.io/`
>5. Specify the `MultiKeys` set `True` if `listTronGridAPIKEY` is used.
>6. Specify the `NETWORK` enter one of the provided networks: `Mainnet`, `ShastaTestnet`, `NileTestnet`

------------
File `config.py`:
>1. `ERROR` - A file that will be created by itself when an error occurs, errors will be written to it. Default: error.txt
>2. `PILLOW` - Created automatically, records the last block that was checked but not sent to the queue. Default: rescue_pillow.json

Search for transactions by node.
--------------
Run script via console

> Run the script from number to number.
>```shell
> python search_in_history_script.py -s startBlockNumber -e endBlockNumber
> python search_in_history_script.py --start startBlockNumber --end endBlockNumber

> Run the script for the block list 
> ```shell
> python search_in_history_script.py -b 'blockNumber blockNumber blockNumber ...'
> python search_in_history_script.py --blocks 'blockNumber blockNumber blockNumber ...'

> Run the script (ONLY WITH '-b --blocks' OR '-s --start -e --end') with the wallet address or addresses
> ```shell
> python search_in_history_script.py -b 'blockNumber blockNumber blockNumber ...' -a walletAddress,walletAddress
> python search_in_history_script.py -s startBlockNumber ...' --addresses walletAddress,walletAddress


> Also allowed.
> ```shell
> python search_in_history_script.py -s startBlockNumber
> python search_in_history_script.py --start startBlockNumber
> 
> python search_in_history_script.py -e endBlockNumber
> python search_in_history_script.py --end endBlockNumber
>
> python search_in_history_script.py -b blockNumber
> python search_in_history_script.py --block blockNumber
> 
> python search_in_history_script.py -e startBlockNumber -a walletAddress,walletAddress
> python search_in_history_script.py -end startBlockNumber --addresses walletAddress,walletAddress

------------------