
JSON API za tečajne liste BSI
=============================

Kratka navodila za namestitev::

    createdb bsi_tecaji

    virtualenv .
    . bin/activate
    pip install -r requirements.txt

    python manage.py migrate
    python manage.py update_bsi --full
    python manage.py runserver

    curl http://127.0.0.1:8000/tecaj/?datum=2015-06-12
    curl http://127.0.0.1:8000/tecaj/?datum=2015-06-12&oznaka=USD

V cron.daily::

    python manage.py update_bsi