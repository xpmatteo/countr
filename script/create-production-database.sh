#!/usr/bin/env bash

dbname="ebdb"
dbuser="countr"
dbpassword=$AWS_COUNTR1_PROD_RDS_PASSWORD
dbhost="aa1fj35qzere6j9.csfpyzhrgihs.eu-west-1.rds.amazonaws.com"

set -e
cd "$(dirname "$0")/.."

cat sql/???_*.sql | mysql -u$dbuser "-p$dbpassword" -h$dbhost $dbname

