#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile


class GstreamerCustomConan(ConanFile):
    name = "gstreamer-custom"
    version = "1.14.0.1"
    description = "custom modified gstreamer library"
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
        self.requires("gstreamer-runtime/%s@%s/stable" %
                      (self.version, os.environ['CONAN_USERNAME']))
        self.requires("gstreamer-dev/%s@%s/stable" %
                      (self.version, os.environ['CONAN_USERNAME']))

    def build(self):
        pass

    #     if self.settings.os == "Linux":
    #         for p in self.deps_cpp_info.build_paths:
    #             self.run("sudo cp -rf build %s/cerbero" % self.root, cwd=p)

    #         self.tar = "gstreamer-1.0-linux-x86_64-%s.tar.bz2" % self.version

    #         self.run(
    #             "if [ ! -f %s ]; then sudo ./cerbero-uninstalled -c \
    #             config/linux.config package gstreamer-1.0 -t; fi" % self.tar,
    #             cwd="%s/cerbero" % self.root)

    # def package(self):
    #     self.copy(pattern=self.tar, dst=".", src="%s/cerbero" % self.root)

    # def package_info(self):
    #     output_dir = os.environ.get("GSTREAMER_1_0_ROOT_X86_64",
    #                                 "/opt/gstreamer/linux_x86_64")
    #     tar_package = "%s/%s" % (os.getcwd(), self.tar)
    #     self.run("mkdir -p %s" % output_dir)
    #     self.run("tar -jxf %s" % tar_package, cwd=output_dir)
