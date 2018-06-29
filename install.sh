#! /bin/bash

if [ `expr $(pkg-config --version) \< 0.29.1` -ne 0 ]; then 
    cd /tmp
    wget https://pkg-config.freedesktop.org/releases/pkg-config-0.29.1.tar.gz
    tar -zxf pkg-config-0.29.1.tar.gz
    cd pkg-config-0.29.1
    ./configure --prefix=/usr        \
                --with-internal-glib \
                --disable-host-tool  \
                --docdir=/usr/share/doc/pkg-config-0.29.1
    make
    sudo make install
fi
