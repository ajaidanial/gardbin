#!/bin/bash

# meta data
config_file="config.json"
backup_file_name="./backups/$(date +%Y-%m-%d-%T)"

# installing dependencies
echo "Setting up dependencies..."

sudo apt install python3 python3-dev python3-pip postgresql libpq-dev \
  virtualenv postgresql-contrib python3-psycopg2 jq

# setup the virtual environment
echo "Setting up environment..."

sudo rm -r venv
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt

# pre back up meta
echo "Setting up the backup..."

mkdir backups
export PGPASSWORD=$(jq '.db_connect.password' ${config_file})

# back up script visit https://gist.github.com/ajaidanial/91724d85bd899e3e4a905fa73a49f8b1 for more info
pg_dump -F t -h $(jq '.db_connect.host' ${config_file}) -U $(jq '.db_connect.user' ${config_file}) \
  $(jq '.db_connect.database' ${config_file}) >${backup_file_name}.backup
gzip $(backup_file_name).backup

# post back up meta
unset PGPASSWORD

# run the main script
python main.py
