#!/usr/bin/env bash

TMP_PATH=/tmp/aurora_update
FINAL_PATH=/home/pi/aurora

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

source install_src

echo -e $c_blue" >>>> Testing internet connection : "$c_def $s_dim

ping -c2 github.com

echo -ne $s_def

if [ "$?" -ne 0 ] ; then
    echo -e $c_red"   >>>> Unable to reach github"$c_def
    exit 1
fi

if [ -d $TMP_PATH ] ; then
    echo -e $c_blue" >>>> Git repo allready exist, cleaning .. "$c_def
    rm -rf $TMP_PATH
fi

echo -e $c_blue" >>>> Cloning git repo in "$s_dim"$TMP_PATH"$c_def

cd /tmp
git clone https://github.com/dprslt/aurora.git $TMP_PATH

echo -ne $s_def


if [ "$?" -ne 0 ] ; then
    echo -e $c_red" >>>> Unable to reach clone github repository "$c_def
    exit 1
fi

echo -e $c_blue" >>>> Comparing last commit hashes"$c_def

cd $FINAL_PATH
current_hash=`git rev-parse HEAD`
cd $TMP_PATH
last_hash=`git rev-parse HEAD`

if [ "$current_hash" == "$last_hash" ] ; then
    echo -e $c_red" >>>>>>>> The last version is already installed"$c_def
    cd /tmp
    rm -rf $TMP_PATH
    exit 1
fi




echo -e $c_blue" >>>> Stoping old daemon"$c_def

cd $FINAL_PATH
sudo ./uninstall.sh


cd $TMP_PATH
echo -e $c_blue" >>>> Launching new daemon"$c_def
sudo ./install.sh


echo -e $c_blue" >>>> Waiting for daemon to boot"$c_def

sleep 5
sudo systemctl status --no-pager -n2 aurora

if [ "$?" -ne 0 ] ; then
    echo -e $c_red" >>>> New version is not working, restoring the old one "$c_def
    sudo ./uninstall.sh
    cd $FINAL_PATH
    sudo ./install.sh
    rm -r $TMP_PATH


    exit 1
fi

echo -e $c_blue" >>>> Daemon seems working well, udating sources"$c_def

rm -r $FINAL_PATH
mv $TMP_PATH $FINAL_PATH
sudo chown -R pi $FINAL_PATH/

echo -e $c_blue" >>>> Done !"$c_def






