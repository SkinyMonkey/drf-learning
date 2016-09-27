## Setup

```
git clone https://github.com/SkinyMonkey/drf-learning.git;
cd drf-learning;
git checkout develop;

virtualenv venv; # On cree un env virtuel
source venv/bin/activate; # On rentre dedans
pip install -r requirements.txt; # equivalent de npm install
mkdir tmp; # pour hoster la db sqlite
python manage.py migrate; # creation des tables SQL en suivant les migration
python manage.py createsuperuser; # je met adrien et lolilollolilol, vous pouvez changer ca sans pb, il faudra juste penser a update les tests
```

Et finalement, pour lancer le serv de dev:

```
python manage.py runserver .
```

Pour lancer les tests lancer le serveur de dev et tapez:

```
python tests/test.py
```
