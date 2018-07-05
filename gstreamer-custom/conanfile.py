#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


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
    build_dir = ""
    generators = "cmake"

    def config_options(self):
        # self.root = "%s" % os.getcwd()
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        self.run("git config --global user.name \"yjjnls\"")
        self.run("git config --global user.email \"x-jj@foxmail.com\"")

    def requirements(self):
        self.requires("gstreamer-runtime/%s@%s/stable" %
                      (self.version, os.environ['CONAN_USERNAME']))
        self.requires("gstreamer-dev/%s@%s/stable" %
                      (self.version, os.environ['CONAN_USERNAME']))
        pass

    def build(self):
        self.run(
            "git clone https://github.com/yjjnls/libgstrtspserver.git --recursive"
        )
        self.build_dir = os.getcwd()
        if self.settings.os == "Linux":
            gstreamer_root = os.environ.get("GSTREAMER_ROOT",
                                            "/opt/gstreamer/linux_x86_64")

            vars = {
                'PKG_CONFIG_PATH': "%s/lib/pkgconfig" % gstreamer_root,
                'GSTREAMER_ROOT': gstreamer_root
            }

            cmake = CMake(self)
            with tools.environment_append(vars):
                self.run(
                    "chmod +x build.sh && sudo ./build.sh",
                    cwd="%s/libgstrtspserver" % os.getcwd())
                cmake.configure(source_folder='libgstrtspserver')
                cmake.build()
                # cmake.install()

    def package(self):
        ext = '.dll'
        if self.settings.os == 'Linux':
            ext = '.so'
        self.copy(pattern="libgstrtspserver-1.0%s" % ext, dst="out", src=".")

    def package_info(self):
        if self.settings.os == "Linux":
            gstreamer_root = os.environ.get("GSTREAMER_ROOT",
                                            "/opt/gstreamer/linux_x86_64")

            self.run("sudo rm -rf out.bak && sudo cp -rf out out.bak")
            self.run("sudo mv out.bak/libgstrtspserver-1.0.so %s/lib" %
                     gstreamer_root)
