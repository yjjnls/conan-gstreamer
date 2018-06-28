#! /bin/bash

git clone https://github.com/GStreamer/cerbero.git
cd cerbero
git checkout 1.14.0.1
./cerbero-uninstalled -c config/linux.config bootstrap