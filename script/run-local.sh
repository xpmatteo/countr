#!/usr/bin/env bash

set -e
cd $(dirname $0)/..


export RDS_DB_NAME=countr_dev
export RDS_HOSTNAME=localhost
export RDS_PORT=3306
export RDS_USERNAME=countr
export RDS_PASSWORD=countr

export FLASK_APP=countr.py
export FLASK_DEBUG=1

exec flask run
