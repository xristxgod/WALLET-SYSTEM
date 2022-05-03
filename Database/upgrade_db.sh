export FLASK_APP=src/wsgi.py
flask db init
flask db stamp head
flask db migrate
flask db upgrad