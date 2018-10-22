#!/usr/bin/env bash
supervisorctl stop all
source venv/bin/activate
git pull

python manage.py migrate --settings=config.settings.production
python manage.py collectstatic --settings=config.settings.production
python manage.py compilemessages -l uk --settings=config.settings.production
python manage.py compilemessages -l en --settings=config.settings.production

supervisorctl start all
