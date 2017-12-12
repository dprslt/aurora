#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

source ./install_src

echo -e $c_green"Stopping service in  : "$s_dim"$SERVICE_PATH"$c_def $s_def
systemctl stop $DAEMON_NAME
systemctl disable $DAEMON_NAME

echo -e $c_green"Removing service in  : "$s_dim"$SERVICE_PATH"$c_def $s_def
rm $SERVICE_PATH.service

echo -e $c_green"Deleting install directory : "$s_dim"$DAEMON_PATH"$c_def $s_def

rm -r $DAEMON_PATH
