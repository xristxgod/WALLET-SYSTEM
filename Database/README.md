Interface for working with the database!
================

> Serves for easier database management. `Creating`, `adding`, `deleting` and `updating` data.

> Launch the interface: 
> ```shell
> # Run the interface:
> python3 ./app.py 
> # Run the interface via docker:
> docker-compose --file database-interface-docker-compose.yml up --build
> # Stop the interface
> docker-compose --file database-interface-docker-compose.yml stop
> # Run the interface through the bash script:
> bash run.sh
> # Stop the interface
> bash stop.sh
> ```

> Create a migration: 
> ``` shell
> # Create a migration: 
> export FLASK_APP=src/wsgi.py
> flask db init
> flask db stamp head
> flask db migrate
> flask db upgrade
> # Or through the bash script
> bash upgrade_db.sh
> ```

API DOCS
-------