The Tron network
===========

##### It is used to work and interact with the Tron network

> `Finance/Tron/api/` - Swaggers for working with the `TRON` network. 
> Creating a wallet/s, viewing the balance of the native and token, and creating and sending transactions of the native and token (The number of tokens will be replenished).

> `Finance/Tron/demon/` - The daemon for continuous operation and tracking user transactions on the `TRON` network.
> When detected, it sends it to RabbitMQ for further work. Works endlessly.