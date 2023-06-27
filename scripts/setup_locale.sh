###################################################
# Setup Locale CFG
###################################################

sudo apt-get update && sudo apt-get install tzdata locales -y && sudo locale-gen pt_BR.UTF-8
sudo localectl set-locale LANG="pt_BR.UTF-8"
export LANG="pt_BR.UTF-8"
sudo update-locale
locale -a
locale
locale -c -k LC_NUMERIC
localectl status
