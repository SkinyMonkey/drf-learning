#!/bin/sh

# Everything needed to start!

virtualenv venv;
source venv/bin/activate;
pip install -r requirements.txt;
mkdir tmp;
python manage.py migrate;

echo "The next command will setup the admin user";
echo "Use adrien for the login and lolilollolilol as the password for the test to work directly";
echo "Otherwise change the login and password in the tests"

# FIXME : inject the entered login and password into the tests
python manage.py createsuperuser;
