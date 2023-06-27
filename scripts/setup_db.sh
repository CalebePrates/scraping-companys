
#!/bin/bash

###################################################
# Setup postgres db and roles
# ref: https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
###################################################

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

called_by=$1

if [ ${called_by:-"manually"} != "setup_venv" ]
then
    echo -e "${RED}This script can not be call manually. So the correct packages have already been installed.${NC}"
else
    echo 'Init postgres handler'
    sudo apt update
    sudo apt-get install libpq-dev postgresql postgresql-contrib
    sudo gpasswd -a postgres ssl-cert
    sudo chown root:ssl-cert  /etc/ssl/private/ssl-cert-snakeoil.key
    sudo chmod 740 /etc/ssl/private/ssl-cert-snakeoil.key

    echo 'Creating db for local development'
    sudo service postgresql start
    sudo -u postgres createuser $(whoami);
    sudo su - postgres <<EOF
        psql
        ALTER USER $(whoami) CREATEDB;

        CREATE DATABASE scraping_local;
        CREATE USER develop WITH PASSWORD 'develop';
        ALTER ROLE develop SET client_encoding TO 'utf8';
        ALTER ROLE develop SET default_transaction_isolation TO 'read committed';
        ALTER ROLE develop SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE scraping_local TO develop;
        GRANT ALL PRIVILEGES ON DATABASE scraping_local TO $(whoami);


        CREATE USER tester WITH PASSWORD 'tester';
        ALTER ROLE tester SET client_encoding TO 'utf8';
        ALTER ROLE tester SET default_transaction_isolation TO 'read committed';
        ALTER ROLE tester SET timezone TO 'UTC';
        ALTER USER tester CREATEDB;

        DROP DATABASE scraping_local;
        ALTER USER $(whoami) WITH SUPERUSER;
        ALTER USER develop WITH SUPERUSER;
        ALTER USER tester WITH SUPERUSER;

EOF

fi

echo -e "${GREEN}Setup DB finished!${NC}"
echo -e "\n"
