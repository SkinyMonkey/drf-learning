#!/bin/sh

# Everything needed to start!

virtualenv venv;
source venv/bin/activate;
pip install -r requirements.txt;
mkdir tmp;
python manage.py migrate;
python manage.py createsuperuser;
