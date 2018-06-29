#! /bin/bash

git clone https://github.com/yjjnls/cerbero
cd cerbero
./cerbero-uninstalled -c config/linux.config bootstrap
./cerbero-uninstalled -c config/linux.config package gstreamer-1.0 -t