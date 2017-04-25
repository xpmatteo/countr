#!/usr/bin/env bash

set -e
cd $(dirname $0)/..


export MYSQL_DATABASE_DB=countr_dev
export MYSQL_DATABASE_HOST=localhost
export MYSQL_DATABASE_USER=countr
export MYSQL_DATABASE_PASSWORD=countr

export FLASK_APP=countr.py
export FLASK_DEBUG=1

exec flask run
