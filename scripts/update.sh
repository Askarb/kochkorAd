#!/bin/bash

source ../../venv/bin/activate
pip install -r ../requirements.txt
cd ../webapp_root
./manage.py migrate
./manage.py collectstatic --noinput
