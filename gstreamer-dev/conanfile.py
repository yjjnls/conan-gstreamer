#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, CMake, tools


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

    def config_options(self):
        self.root = "%s/.." % os.getcwd()
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def requirements(self):
        if not os.path.exists("%s/cerbero" % self.root):
            self.run("git clone https://github.com/yjjnls/cerbero",
                     cwd=self.root)
        self.run("git config --global user.name \"yjjnls\"")
        self.run("git config --global user.email \"x-jj@foxmail.com\"")

        self.requires("gstreamer-build-tools/%s@%s/stable" %
                      (self.version, os.environ['CONAN_USERNAME']))
        # self.requires("gstreamer-package/%s@%s/stable" %
        #               (self.version, os.environ['CONAN_USERNAME']))

    def build(self):
        if self.settings.os == "Linux":
            # self.run("sudo mkdir -p %s/cerbero/build/build-tools" % self.root)
            self.run(
                "sudo cp -rf build %s/cerbero" % self.root,
                cwd=self.deps_cpp_info["gstreamer-build-tools"].build_paths[0])
            self.run(
                "sudo ./cerbero-uninstalled -c config/linux.config shell && which autoconf",
                cwd="%s/cerbero" % self.root)
            # self.run("sudo mkdir -p %s/cerbero/build/sources" % self.root)
            # self.run(
            #     "sudo cp -rf build %s/cerbero" % self.root,
            #     cwd=self.deps_cpp_info["gstreamer-package"].build_paths[0])
            self.run("sudo rm -rf *tar*", cwd="%s/cerbero" % self.root)
            self.run(
                "sudo ./cerbero-uninstalled -c config/linux.config package gstreamer-1.0 -t",
                cwd="%s/cerbero" % self.root)

    def package(self):
        tar = "gstreamer-1.0-linux-x86_64-%s-devel.tar.bz2" % self.version
        # self.copy(pattern=tar, dst=".", src="%s/cerbero" % self.root)
