TRON DEMON for Python
===================

Search for Tron transactions in a transaction array of addresses.

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
