#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from conans import ConanFile


class GstreamerRuntimeConan(ConanFile):
    name = "gstreamer-runtime"
    version = "1.14.0.1"
    description = "gstreamer runtime library"
    url = "https://github.com/yjjnls/conan-gstreamer"
    license = "Apache-2.0"
    homepage = "https://github.com/yjjnls/conan-gstreamer"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=True"
    source_subfolder = "source_subfolder"
    root = ""
    tar = ""

    def config_options(self):
        self.root = "%s/.." % os.getcwd()
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        if not os.path.exists("%s/cerbero" % self.root):
            self.run(
                "git clone https://github.com/yjjnls/cerbero", cwd=self.root)
        self.run("git config --global user.name \"yjjnls\"")
        self.run("git config --global user.email \"x-jj@foxmail.com\"")

    def requirements(self):
        self.requires("gstreamer-build-tools/%s@%s/stable" %
                      (self.version, os.environ['CONAN_USERNAME']))
        self.requires("gstreamer-package/%s@%s/stable" %
                      (self.version, os.environ['CONAN_USERNAME']))

    def build(self):
        if self.settings.os == "Linux":
            for p in self.deps_cpp_info.build_paths:
                self.run("sudo cp -rf build %s/cerbero" % self.root, cwd=p)

            self.tar = "gstreamer-1.0-linux-x86_64-%s.tar.bz2" % self.version

            self.run(
                "if [ ! -f %s ]; then sudo ./cerbero-uninstalled -c \
                config/linux.config package gstreamer-1.0 -t; fi" % self.tar,
                cwd="%s/cerbero" % self.root)

    def package(self):
        self.copy(pattern=self.tar, dst=".", src="%s/cerbero" % self.root)

    def package_info(self):
        if self.settings.os == "Linux":
            self.tar = "gstreamer-1.0-linux-x86_64-%s.tar.bz2" % self.version

            gstreamer_root = os.environ.get("GSTREAMER_ROOT",
                                            "/opt/gstreamer/linux_x86_64")
            tar_package = "%s/%s" % (os.getcwd(), self.tar)
            self.run("mkdir -p %s" % gstreamer_root)
            self.run("tar -jxf %s" % tar_package, cwd=gstreamer_root)
            for top, dirs, nondirs in os.walk(
                    "%s/lib/pkgconfig" % gstreamer_root):
                for item in nondirs:
                    self.replace_pc(os.path.join(top, item), gstreamer_root)

            self.install_tshell()

    def replace_pc(self, target_file, target_dir):
        file_object = open(target_file, 'r+')
        pattern = ""
        try:
            all_lines = file_object.readlines()
            file_object.seek(0)
            file_object.truncate()
            for line in all_lines:
                if 'cerbero/build/dist/linux_x86_64' in line:
                    searchObj = re.search(
                        '(.*)=(.*)cerbero/build/dist/linux_x86_64', line)
                    if searchObj:
                        pattern = "%scerbero/build/dist/linux_x86_64" % searchObj.group(
                            2)
                        line = line.replace("%scerbero/build/dist/linux_x86_64"
                                            % searchObj.group(2), target_dir)
                    else:
                        line = line.replace(pattern, target_dir)
                file_object.write(line)
        finally:
            file_object.close()

    def install_tshell(self):
        if self.settings.os == "Linux":
            gstreamer_root = os.environ.get("GSTREAMER_ROOT",
                                            "/opt/gstreamer/linux_x86_64")
            content = "#!/bin/bash\n\nexport GSTREAMER_ROOT=$(pwd)\nexport CPPFLAGS=\"-I${GSTREAMER_ROOT}/include ${CPPFLAGS}\"\nexport GST_REGISTRY_1_0=\"${HOME}/.cache/gstreamer-1.0/gstreamer-cerbero-registry\"\nexport XDG_CONFIG_DIRS=\"${GSTREAMER_ROOT}/etc/xdg${XDG_CONFIG_DIRS:+:$XDG_CONFIG_DIRS}:/etc/xdg\"\nexport LDFLAGS=\"-L${GSTREAMER_ROOT}/lib ${LDFLAGS}\"\nexport XDG_DATA_DIRS=\"${GSTREAMER_ROOT}/share${XDG_DATA_DIRS:+:$XDG_DATA_DIRS}:/usr/local/share:/usr/share\"\nexport GST_PLUGIN_SYSTEM_PATH_1_0=\"${GSTREAMER_ROOT}/lib/gstreamer-1.0\"\nexport GIO_EXTRA_MODULES=\"${GSTREAMER_ROOT}/lib/gio/modules\"\nexport GST_PLUGIN_SYSTEM_PATH=\"${GSTREAMER_ROOT}/lib/gstreamer-0.10\"\nexport GST_PLUGIN_SCANNER=\"${GSTREAMER_ROOT}/libexec/gstreamer-0.10/gst-plugin-scanner\"\nexport GST_PLUGIN_SCANNER_1_0=\"${GSTREAMER_ROOT}/libexec/gstreamer-1.0/gst-plugin-scanner\"\nexport CFLAGS=\"-I${GSTREAMER_ROOT}/include ${CFLAGS}\"\nexport PYTHONPATH=\"${GSTREAMER_ROOT}/lib/python2.7/site-packages${PYTHONPATH:+:$PYTHONPATH}\"\nexport PKG_CONFIG_PATH=\"${GSTREAMER_ROOT}/lib/pkgconfig:${GSTREAMER_ROOT}/share/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}\"\nexport PATH=\"${GSTREAMER_ROOT}/bin${PATH:+:$PATH}:/usr/local/bin:/usr/bin:/bin\"\nexport GST_REGISTRY=\"${HOME}/.gstreamer-0.10/gstreamer-cerbero-registry\"\nexport LD_LIBRARY_PATH=\"${GSTREAMER_ROOT}/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}\"\nexport CXXFLAGS=\"-I${GSTREAMER_ROOT}/include ${CXXFLAGS}\"\nexport GI_TYPELIB_PATH=\"${GSTREAMER_ROOT}/lib/girepository-1.0\"\n\n$SHELL \"$@\""

            self.run("echo \"%s\" >%s/tshell.sh" % (content, gstreamer_root))
