#!/bin/bash

###################################################
# Setup Virtual Env Credmei API
###################################################

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

package_installer()
{
    result=$(dpkg --get-selections | grep $1 )
    if [ -n "${result}" ]
    then
        echo '*****************************************'
        echo 'Installing the package '$1''
        $2
        echo 'end of package installation'
        echo '*****************************************'
        echo
    fi
}

echo 'Installing linux dependency packages'
sudo apt-get update && sudo apt-get upgrade -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install -y python3.11

sudo apt install -y python3-pip
pip install psycopg2-binary

echo 'Installing project dependency packages'
package_installer 'python3.11' 'sudo apt-get install python3.11'
package_installer 'python3.11-dev' 'sudo apt install python3.11-dev'
package_installer 'pip' 'sudo pip install -U pip --user'
package_installer 'virtualenv' 'sudo pip install virtualenv'

# Postgres db and users
. ./scripts/setup_db.sh setup_venv

# Cria a venv
if [ ! -d venv ]
then
    echo 'Setting up virtualenv...'
    virtualenv -p python3.11 venv
fi

source venv/bin/activate
pip install --upgrade pip
echo 'Installing python dependencies...'
pip install -r ./requirements/local.txt

echo -e "${GREEN}"
echo '========================================='
echo '   Instalações concluídas com sucesso!   '
echo '========================================='
echo -e "${NC}"

echo -e "${GREEN}Pronto! Feche este terminal e abra outro!${NC}"
echo -e "\n"
