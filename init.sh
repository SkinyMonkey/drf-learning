#!/bin/sh

# Everything needed to start!

virtualenv venv;
source venv/bin/activate;
pip install -r requirements.txt;
mkdir -p tmp/data;
python manage.py migrate;
python manage.py loaddata whyd/fixtures/users.json

echo "Login : adrien, Password: agricool"
