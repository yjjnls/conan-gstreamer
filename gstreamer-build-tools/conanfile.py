#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
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
        self.run(
            "if [ ! -d cerbero ]; then git clone https://github.com/yjjnls/cerbero; fi",
            cwd=self.root)
        self.run("git config --global user.name \"yjjnls\"")
        self.run("git config --global user.email \"x-jj@foxmail.com\"")

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

    def package(self):
        self.copy(
            pattern="*",
            dst="build",
            src="%s/cerbero/build" % self.root,
            symlinks=True)

    # def package_info(self):
    #     if self.settings.os == "Linux":
    #         self.run("sudo cp -rf %s/cerbero/build %s" % (self.root,
    #                                                       os.getcwd()))
