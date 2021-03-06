#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from conans import CMake, ConanFile, tools


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
    generators = "cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        pass

    def requirements(self):
        self.requires("gstreamer-runtime/%s@%s/stable" %
                      (self.version, os.environ.get("DEPENDENT_BINTRAY_REPO")))

    def build_requirements(self):
        if self.settings.os == "Linux":
            self.build_requires("gstreamer-dev/%s@%s/stable" %
                                (self.version, os.environ.get("DEPENDENT_BINTRAY_REPO")))

    def build(self):
        self.run(
            "git clone https://github.com/yjjnls/libgstrtspserver.git --recursive"
        )
        self.run("git clone https://github.com/yjjnls/libgstwebrtc.git \
            && cd libgstwebrtc && git submodule update --init")

        if self.settings.os == "Linux":
            gstreamer_root = os.environ.get(
                "GSTREAMER_ROOT",
                "%s/gstreamer/linux_x86_64" % os.getenv("HOME"))

            vars = {
                'PKG_CONFIG_PATH': "%s/lib/pkgconfig" % gstreamer_root,
                'GSTREAMER_ROOT': gstreamer_root
            }

            self.run(
                "chmod +x build.sh && sudo ./build.sh",
                cwd="%s/libgstrtspserver" % os.getcwd())

        cmake = CMake(self)
        with tools.environment_append(vars):
            # rtsp-server
            cmake.configure(
                source_folder='libgstrtspserver',
                build_folder='build/rtspserver')
            cmake.build(build_dir='build/rtspserver')

            # webrtc
            cmake.configure(
                source_folder='libgstwebrtc/dtls', build_folder='build/dtls')
            cmake.build(build_dir='build/dtls')

    def package(self):
        ext = '.dll'
        if self.settings.os == 'Linux':
            ext = '.so'
        self.copy(
            pattern="libgstrtspserver-1.0%s" % ext,
            dst="out",
            src="build/rtspserver")
        self.copy(pattern="libgstdtls%s" % ext, dst="out", src="build/dtls")

    def package_info(self):
        if self.settings.os == "Linux":
            gstreamer_root = os.environ.get(
                "GSTREAMER_ROOT",
                "%s/gstreamer/linux_x86_64" % os.getenv("HOME"))

            self.run("sudo rm -rf out.bak && sudo cp -rf out out.bak")
            self.run("sudo mv out.bak/libgstrtspserver-1.0.so %s/lib" %
                     gstreamer_root)
            self.run("sudo mv out.bak/libgstdtls.so %s/lib/gstreamer-1.0" %
                     gstreamer_root)
            self.run("sudo rm -rf out.bak")
