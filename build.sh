#! /bin/bash

git clone https://github.com/yjjnls/cerbero
cd cerbero
yes|sudo ./cerbero-uninstalled -c config/linux.config bootstrap
sudo rm -rf *tar.bz2
sudo ./cerbero-uninstalled -c config/linux.config package gstreamer-1.0 -t