#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, CMake, tools


class GstreamerDevelopmentConan(ConanFile):
    name = "gstreamer-package"
    version = "1.14.0.1"
    description = "source package for gstreamer build in cerbero"
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
            self.run(
                "git clone https://github.com/yjjnls/cerbero", cwd=self.root)

    def build(self):
        if self.settings.os == "Linux":
            self.run(
                "sudo ./cerbero-uninstalled -c config/linux.config fetch-package gstreamer-1.0 --deps",
                cwd="%s/cerbero" % self.root)

    def package(self):
        self.copy(
            pattern="local",
            dst=".",
            src="%s/cerbero/build/source" % self.root)
