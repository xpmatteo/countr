#!/usr/bin/env bash

# Create local development and test databases
# If they exist, drop them and recreate them from scratch. No warning will be given!

# define key information
dbname="countr"

# no customization needed beyond this line
dbname_dev=${dbname}_dev
dbname_test=${dbname}_test
dbuser=${dbname}
dbpassword=${dbname}

set -e
cd "$(dirname "$0")/.."

read -s -p "mysql root password? (type return for no password) " MYSQL_ROOT_PASSWORD
if [ "$MYSQL_ROOT_PASSWORD" != "" ]; then
    MYSQL_ROOT_PASSWORD=-p$MYSQL_ROOT_PASSWORD
fi

mysqladmin -uroot $MYSQL_ROOT_PASSWORD --force drop $dbname_dev   || true
mysqladmin -uroot $MYSQL_ROOT_PASSWORD --force drop $dbname_test  || true

echo "create database $dbname_dev  default charset utf8;" | mysql -uroot $MYSQL_ROOT_PASSWORD
echo "create database $dbname_test default charset utf8;" | mysql -uroot $MYSQL_ROOT_PASSWORD

echo "grant all on $dbname_dev.*  to '$dbuser'@localhost identified by '$dbpassword';" \
     | mysql -uroot $MYSQL_ROOT_PASSWORD
echo "grant all on $dbname_test.* to '$dbuser'@localhost identified by '$dbpassword';" \
     | mysql -uroot $MYSQL_ROOT_PASSWORD

echo "$dbname_dev created"
echo "$dbname_test created"
