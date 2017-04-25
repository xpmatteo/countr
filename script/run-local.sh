#!/usr/bin/env bash

set -e
cd $(dirname $0)/..

export FLASK_APP=countr.py
export FLASK_DEBUG=1
exec flask run
