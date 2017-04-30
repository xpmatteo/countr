#!/usr/bin/env bash

# define key information
dbname="countr_prod"
dbuser="countr"
dbpassword="cheigiyoo2Ooghee"
dbhost="countr-prod.csfpyzhrgihs.eu-west-1.rds.amazonaws.com"

set -e
cd "$(dirname "$0")/.."

cat sql/???_*.sql | mysql -u$dbuser "-p$dbpassword" -h$dbhost $dbname

