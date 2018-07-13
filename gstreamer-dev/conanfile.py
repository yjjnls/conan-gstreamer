#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from conans import ConanFile


class GstreamerDevelopmentConan(ConanFile):
    name = "gstreamer-dev"
    version = "1.14.0.1"
    description = "gstreamer library for development"
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

    def build_requirements(self):
        if self.settings.os == "Linux":
            self.build_requires("gstreamer-build-tools/%s@%s/stable" %
                                (self.version, os.environ.get("DEPENDENT_BINTRAY_REPO", os.environ.get("CONAN_USERNAME"))))

    def build(self):
        if self.settings.os == "Linux":
            for p in self.deps_cpp_info.build_paths:
                self.run("sudo cp -rf build %s/cerbero" % self.root, cwd=p)

            self.tar = "gstreamer-1.0-linux-x86_64-%s-devel.tar.bz2" % self.version

            self.run(
                "if [ ! -f %s ]; then sudo ./cerbero-uninstalled -c \
                config/linux.config package gstreamer-1.0 -t; fi" % self.tar,
                cwd="%s/cerbero" % self.root)

    def package(self):
        self.copy(pattern=self.tar, dst=".", src="%s/cerbero" % self.root)

    def package_info(self):
        if self.settings.os == "Linux":
            self.tar = "gstreamer-1.0-linux-x86_64-%s-devel.tar.bz2" % self.version

            gstreamer_root = os.environ.get(
                "GSTREAMER_ROOT",
                "%s/gstreamer/linux_x86_64" % os.getenv("HOME"))
            tar_package = "%s/%s" % (os.getcwd(), self.tar)
            self.run("sudo mkdir -p %s" % gstreamer_root)
            self.run("sudo tar -jxf %s" % tar_package, cwd=gstreamer_root)
            self.run(
                "sudo chmod 666 *", cwd="%s/lib/pkgconfig" % gstreamer_root)
            for top, dirs, nondirs in os.walk(
                    "%s/lib/pkgconfig" % gstreamer_root):
                for item in nondirs:
                    self.replace_pc(os.path.join(top, item), gstreamer_root)

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
