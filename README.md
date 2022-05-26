Crypto wallet for Telegram
====
:::: `Start date of development: April 18, 2022` :::: `DEVELOPMENT` :::: `End date of development: January 25, 2023` ::::

---
> This service will be a crypto wallet that is somewhat similar to `Trust Wallet` and `similar`. 
> But only in the telegram social network, for ease of work. My plans are to add such blockchain 
> currencies as (BTC, ETH, BSC, TRON and SOLANA) and, in addition to native currencies,
> their remaining tokens (smart contracts). The developer also has an admin panel, a service for monitoring prices 
> for cryptocurrencies (exchange rate). Buying and selling for real money. I have no deadlines and I'm doing it on pure
> enthusiasm. The code is completely open and you can take it. I plan to use all my knowledge and skills. And use 
> new telegram features such as `Payment platform`-`https://core.telegram.org/bots/payments`.

---
Technologies:
-----

> Languages I use: `PYTHON`, `JS`, `BASH`.

> But it is based on Python and its frameworks: `FastApi`, `Django`, `Django REST API`, `AIOGram`, `Celery`, `ASYNCpg`, `AIOPika`, `Pika`, `Psycopg2`.

> Helper frameworks:  `Pydantic`, `emoji`.

> Async helper frameworks: `AIOHttp`, `AIOfiles`.

> Crypto frameworks: `TronPy`, `Web3`, `HDwallet`.

> Other: `Docker`, `Radis`, `RabbitMQ`, `Cron`.
---

> `DatabaseInterface` - Database-Admin panel

> `Bots` - The main bot and the bot for notifications.

> `Finance` - Working with finance and cryptocurrency.

> `Services` - Services for correct operation of the system.

---------
Launch instructions:
####### PS. In the `dev-docker-compose.yml` container, I have assembled the entire project to run on one machine. But for the best work, it is necessary to divide each module into separate containers!
> 1. Fill in your configurations in the `.dev.env` file
> 2. Launch the docker container!

> ```shell
> # Run 
> docker-compose --file dev-docker-compose.yml up --build
> # Stop
> docker-compose --file dev-docker-compose.yml stop
> ```

###### My information will change!!!


