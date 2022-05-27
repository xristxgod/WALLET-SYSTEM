Database interface
======

> This service is needed for:
>> 1. Work with the database, manual modification, addition and deletion of data from it.
>> 2. REST for communication with other services.
>> 3. Administration.

## API ROUTES:

> Find out the exchange rate for the currency.
>> `POST`:`https://<domain>/api/check/coinToCoin/`
> 
> Body:
>> ```
>> {
>>  "coin": str,
>>  "toCoin": Optional[str]
>> }
>> ```
> 
> Response:
>> ```
>> {
>>  "price": float
>> }
>> ```
---------------------------------------------------------------------------------------------
> Create a crypto wallet. (If there is no account, then it will enter it into the system!)
>> `POST`:`https://<domain>/api/create/wallet/`
> 
> Body:
>> ```
>> {
>>  "chatID": str,                    // Telegram user id.
>>  "username": str,                  // Telegram user username.
>>  "network": str,                   // Network name. Example: TRON
>>  "passphrase": Optional[str],      // The secret word for the wallet.
>>  "mnemonicWords": Optional[str]    // Secret mnemonic phrases for generating a wallet.
>> }
>> ```
> 
> Response:
>> ```
>> {
>>  "message": bool
>> }
>> ```
---------------------------------------------------------------------------------------------
> Get the balance of a crypto wallet. (Only those that are in the system!)
>> `POST`:`https://<domain>/api/balance/`
> 
> Body:
>> ```
>> {
>>  "chatID": str,                    // Telegram user id.
>>  "network": str,                   // Network name and Token name. Example: TRON-TRX, TRON-USDT
>>  "address": Optional[str],         // The address of the crypto wallet.
>>  "convert": Optional[List[str]]    // The list of currencies to be converted to. Example: ["usd", "rub"]
>> }
>> ```
> 
> Response:
>> ```
>> {
>>  "balance": float,
>>  "network": str,                           // Network name and Token name. Example: TRON-TRX, TRON-USDT
>>  "convert": Optional[Dict[str, float]      // Example: [{"balanceUSD": 0.001, "balanceRUB": 0.122}]
>> }
>> ```
---------------------------------------------------------------------------------------------
> Create a transaction inside our network. (Not in the blockchain!!!)
>> `POST`:`https://<domain>/api/create/transaction/`
> 
> Body:
>> ```
>> {
>>  "chatID": str,                        // Telegram user id.
>>  "network": str,                       // Network name and Token name. Example: TRON-TRX, TRON-USDT
>>  "inputs": Optional[List[str]],        // Wallets from which transactions will be sent.
>>  "outputs": List[Dict[str, float]],    // Wallets to which the transaction will be sent.
>>  "fee": Optional[List[str]]            // Commission for the transaction. (Not necessarily in this route!)
>> }
>> ```
> 
> Response:
>> ```
>> {
>>  "fee": float                           // Commission for the transaction
>> }
>> ```
---------------------------------------------------------------------------------------------
> Send a transaction to the blockchain network. (Send to the next microservice to work with the transaction!)
>> `POST`:`https://<domain>/api/send/transaction/`
> 
> Body:
>> ```
>> {
>>  "chatID": str,                        // Telegram user id.
>>  "network": str,                       // Network name and Token name. Example: TRON-TRX, TRON-USDT
>>  "inputs": Optional[List[str]],        // Wallets from which transactions will be sent.
>>  "outputs": List[Dict[str, float]],    // Wallets to which the transaction will be sent.
>>  "fee": Optional[List[str]]            // Expected transaction fee! (Required. Otherwise, if the commission grows, the transaction will still be sent)
>> }
>> ```
> 
> Response:
>> ```
>> {
>>  "message": bool                           
>> }
>> ```

---------------------------------------------------------------------------------------------
## SYSTEM API ROUTES

---------------------------------------------------------------------------------------------
> Check the system's operability.
>> `GET`:`https://<domain>/api/health/check/isWork`
> 
> Body:
>> ```
>>  null
>> ```
> 
> Response:
>> ```
>> {
>>  "message": bool                           
>> }
>> ```
---------------------------------------------------------------------------------------------
> Check the operability of the database.
>> `GET`:`https://<domain>/api/health/check/database`
> 
> Body:
>> ```
>>  null
>> ```
> 
> Response:
>> ```
>> {
>>  "message": bool                           
>> }
>> ```
---------------------------------------------------------------------------------------------
> Check the operability and cache class for collecting transactions.
>> `GET`:`https://<domain>/api/check/transaction/cache`
> 
> Body:
>> ```
>>  null
>> ```
> 
> Response:
>> ```
>> {
>>  "repositoryCacheCount": int,          // The number of transactions pending.
>>  "repositoryCacheData": Dict,          // Transactions that are waiting, in an expanded form!
>>  "message": bool                                  
>> }
>> ```