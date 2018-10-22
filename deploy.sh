#!/usr/bin/env bash
echo 'Stopping server...'
supervisorctl stop all
source venv/bin/activate
echo 'Pulling...'
git pull
echo 'Migrating...'
python manage.py migrate --settings=config.settings.production
echo 'Collecting...'
python manage.py collectstatic --no-input --settings=config.settings.production
echo 'Translating...'
python manage.py compilemessages -l uk --settings=config.settings.production
python manage.py compilemessages -l en --settings=config.settings.production
echo 'Starting...'
supervisorctl start all
