#!/bin/bash

sudo apt install python3 python3-dev python3-pip postgresql libpq-dev \
  virtualenv postgresql-contrib python3-psycopg2

sudo rm -r venv
virtualenv -p python3 venv
. venv/bin/activate

pip install -r requirements.txt
python main.py
