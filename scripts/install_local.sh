#!/bin/bash
if [ ! -d "venv" ]; then
virtualenv --no-site-packages --distribute venv
fi
. ./venv/bin/activate
pip install -r requirements.txt
python webapp_root/manage.py migrate
webapp_root/manage.py collectstatic --noinput
cd webapp_root/webapp/
django-admin compilemessages
cd ../../
