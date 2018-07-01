#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, CMake, tools


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

    def config_options(self):
        self.root = "%s/.." % os.getcwd()
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def requirements(self):
        self.run(
            "if [ ! -d cerbero ]; then git clone https://github.com/yjjnls/cerbero; fi",
            cwd=self.root)

        self.requires(
            "gstreamer-build-tools/%s@bincrafters/stable" % self.version)

    def build(self):
        if self.settings.os == "Linux":
            self.run(
                "sudo cp -rf bin include lib share %s/cerbero/build/build-tools"
                % self.root,
                cwd=self.deps_cpp_info.build_paths[0])
            self.run("sudo rm -rf *tar*", cwd="%s/cerbero" % self.root)
            self.run(
                "sudo ./cerbero-uninstalled -c config/linux.config package gstreamer-1.0 -t",
                cwd="%s/cerbero" % self.root)

    def package(self):
        tar = "gstreamer-1.0-linux-x86_64-%s.tar.bz2" % self.version
        self.copy(pattern=tar, dst=".", src="%s/cerbero" % self.root)

    def package_info(self):
        tar = "gstreamer-1.0-linux-x86_64-%s.tar.bz2" % self.version
        self.run("tar -xf %s && sudo rm -f %s" % (tar, tar), cwd=".")
