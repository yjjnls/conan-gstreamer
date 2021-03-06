#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import re
from conans import ConanFile, CMake, tools


class GstreamerBuildToolsConan(ConanFile):
    name = "gstreamer-build-tools"
    version = "1.14.0.1"
    description = "cerbero build tools generated by boostrap"
    url = "https://github.com/yjjnls/conan-gstreamer"
    license = "Apache-2.0"
    homepage = "https://github.com/yjjnls/conan-gstreamer"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=True"
    source_subfolder = "source_subfolder"
    root = ""

    def config_options(self):
        self.root = "%s/.." % os.getcwd()
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def system_requirements(self):
        if not os.path.exists("%s/cerbero" % self.root):
            self.run(
                "git clone https://github.com/yjjnls/cerbero", cwd=self.root)

    def build(self):
        if self.settings.os == "Linux":
            command = "if [ $(dpkg -l |grep build-essential |wc -l) -eq 0 ]; then \
            sudo apt-get -y update && \
            sudo apt-get -y upgrade && \
            yes|sudo apt-get install build-essential; \
            fi "

            self.run(command)
            self.run(
                "yes|sudo ./cerbero-uninstalled -c config/linux.config bootstrap",
                cwd="%s/cerbero" % self.root)
        else:
            path = "%s/cerbero" % self.root
            path = path.replace(":/", ":\\")
            pattern = re.compile(r'([a-z]):\\', re.IGNORECASE)
            path = pattern.sub('/\\1/', path).replace('\\', '/')

            if self.settings.arch == 'x86_64':
                config = 'win64'
            else:
                config = 'win32'
            self.run(
                "cd %s && ./cerbero-uninstalled -c config/%s.cbc bootstrap"
                % (path, config),
                win_bash=True)

    def package(self):
        self.copy(
            pattern="*",
            dst="build",
            src="%s/cerbero/build" % self.root,
            symlinks=True)

    def package_info(self):
        if self.settings.os == "Linux":
            self.run("if [ $(ls /usr/lib/x86_64-linux-gnu|grep -i x11|wc -l) -eq 0 ]; then sudo apt-get -y update; sudo apt-get -y upgrade; sudo apt-get install -y at bison build-essential chrpath cmake cmake-data curl dconf-gsettings-backend dconf-service dctrl-tools devscripts diffstat distro-info-data docbook docbook-dsssl docbook-to-man docbook-xml docbook-xsl doxygen dput fakeroot flex fontconfig-config fonts-dejavu-core g++ g++-4.8 gawk ghostscript glib-networking glib-networking-common glib-networking-services gnome-common gperf gsettings-desktop-schemas gsfonts gtk-doc-tools hardening-includes intltool jade libapr1 libaprutil1 libapt-pkg-perl libarchive-zip-perl libarchive13 libasound2 libasound2-data libasound2-dev libasyncns0 libauthen-sasl-perl libautodie-perl libavahi-client-dev libavahi-client3 libavahi-common-data libavahi-common-dev libavahi-common3 libbison-dev libboost-system1.54.0 libclass-accessor-perl libclone-perl libcommon-sense-perl libcups2 libcupsfilters1 libcupsimage2 libcurl3 libdbus-1-dev libdbus-glib-1-dev libdconf1 libdigest-hmac-perl libdistro-info-perl libdrm-amdgpu1 libdrm-dev libdrm-intel1 libdrm-nouveau2 libdrm-radeon1 libegl1-mesa libegl1-mesa-dev libegl1-mesa-drivers libelf1 libelfg0 libemail-valid-perl libencode-locale-perl libexporter-lite-perl libfakeroot libfile-basedir-perl libfile-listing-perl libfl-dev libflac8 libfont-afm-perl libfontconfig1 libfreetype6 libfuse-dev libfuse2 libgbm1 libgl1-mesa-dev libgl1-mesa-dri libgl1-mesa-glx libglapi-mesa libglib2.0-bin libglib2.0-dev libglu1-mesa libglu1-mesa-dev libgs9 libgs9-common libhtml-form-perl libhtml-format-perl libhtml-parser-perl libhtml-tagset-perl libhtml-tree-perl libhttp-cookies-perl libhttp-daemon-perl libhttp-date-perl libhttp-message-perl libhttp-negotiate-perl libijs-0.35 libintl-perl libio-html-perl libio-pty-perl libio-socket-inet6-perl libio-socket-ssl-perl libio-string-perl libio-stringy-perl libipc-run-perl libipc-system-simple-perl libjbig0 libjbig2dec0 libjpeg-turbo8 libjpeg8 libjson-perl libjson-xs-perl liblcms2-2 liblist-moreutils-perl libllvm3.4 liblwp-mediatypes-perl liblwp-protocol-https-perl liblzo2-2 libmailtools-perl libmirclient-dev libmirclient7 libmirclientplatform-mesa libmirprotobuf-dev libmirprotobuf0 libnet-dns-perl libnet-domain-tld-perl libnet-http-perl libnet-ip-perl libnet-smtp-ssl-perl libnet-ssleay-perl libnetpbm10 libnettle4 libogg0 libopenvg1-mesa libpaper-utils libpaper1 libparse-debcontrol-perl libparse-debianchangelog-perl libpciaccess0 libpcre3-dev libpcrecpp0 libperlio-gzip-perl libprotobuf-dev libprotobuf-lite8 libprotobuf8 libproxy1 libpthread-stubs0-dev libpulse-dev libpulse-mainloop-glib0 libpulse0 libselinux1-dev libsepol1-dev libserf-1-1 libsndfile1 libsocket6-perl libsp1c2 libstdc++-4.8-dev libsub-identify-perl libsub-name-perl libsvn1 libtext-levenshtein-perl libtext-unidecode-perl libtie-ixhash-perl libtiff5 libtxc-dxtn-s2tc0 liburi-perl libvorbis0a libvorbisenc2 libwayland-client0 libwayland-cursor0 libwayland-dev libwayland-egl1-mesa libwayland-server0 libwrap0 libwww-perl libwww-robotrules-perl libx11-6 libx11-data libx11-dev libx11-doc libx11-xcb-dev libx11-xcb1 libxau-dev libxau6 libxcb-dri2-0 libxcb-dri2-0-dev libxcb-dri3-0 libxcb-dri3-dev libxcb-glx0 libxcb-glx0-dev libxcb-present-dev libxcb-present0 libxcb-randr0 libxcb-randr0-dev libxcb-render0 libxcb-render0-dev libxcb-shape0 libxcb-shape0-dev libxcb-sync-dev libxcb-sync1 libxcb-xfixes0 libxcb-xfixes0-dev libxcb1 libxcb1-dev libxcomposite-dev libxcomposite1 libxdamage-dev libxdamage1 libxdmcp-dev libxdmcp6 libxext-dev libxext6 libxfixes-dev libxfixes3 libxi-dev libxi6 libxkbcommon0 libxml-libxml-perl libxml-namespacesupport-perl libxml-parser-perl libxml-sax-base-perl libxml-sax-expat-perl libxml-sax-perl libxml-simple-perl libxpm4 libxrandr-dev libxrandr2 libxrender-dev libxrender1 libxshmfence-dev libxshmfence1 libxslt1.1 libxtst-dev libxtst6 libxv-dev libxv1 libxxf86vm-dev libxxf86vm1 lintian mesa-common-dev mircommon-dev netpbm patchutils poppler-data python3-chardet python3-debian python3-magic python3-pkg-resources python3-six sgml-data sp strace subversion t1utils tcpd texinfo transfig unzip wdiff x11-common x11proto-composite-dev x11proto-core-dev x11proto-damage-dev x11proto-dri2-dev x11proto-fixes-dev x11proto-gl-dev x11proto-input-dev x11proto-kb-dev x11proto-randr-dev x11proto-record-dev x11proto-render-dev x11proto-video-dev x11proto-xext-dev x11proto-xf86vidmode-dev xorg-sgml-doctools xsltproc xtrans-dev xutils-dev yasm; fi")
