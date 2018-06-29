#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, CMake, tools


class TesseractConan(ConanFile):
    name = "gstreamer"
    version = "1.14.0.1"
    description = "conan build for gstreamer"
    url = "https://github.com/yjjnls/conan-gstreamer"
    license = "Apache-2.0"
    homepage = "https://github.com/yjjnls/conan-gstreamer"
    # exports = ["LICENSE.md"]
    # exports_sources = ["build.sh"]
    # generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=True"
    source_subfolder = "source_subfolder"
    root = ""

    # def source(self):
    #     tools.get(
    #         "https://github.com/tesseract-ocr/tesseract/archive/%s.tar.gz" %
    #         self.version)
    #     os.rename("tesseract-" + self.version, self.source_subfolder)
    #     os.rename(
    #         os.path.join(self.source_subfolder, "CMakeLists.txt"),
    #         os.path.join(self.source_subfolder, "CMakeListsOriginal.txt"))
    #     shutil.copy("CMakeLists.txt",
    #                 os.path.join(self.source_subfolder, "CMakeLists.txt"))

    # def configure(self):
    #     self.options["leptonica"].shared = True

    def config_options(self):
        self.root = os.getcwd()
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def system_requirements(self):
        if self.settings.os == "Linux":
            self.run("chmod +x install.sh && ./install.sh")

    def build(self):
        if self.settings.os == "Linux":
            self.run("chmod +x build.sh && sudo ./build.sh", cwd=self.root)

    # def package(self):
    #     self.copy(
    #         "LICENSE",
    #         src=self.source_subfolder,
    #         dst="licenses",
    #         ignore_case=True,
    #         keep_path=False)
    #     # remove man pages
    #     shutil.rmtree(
    #         os.path.join(self.package_folder, 'share', 'man'),
    #         ignore_errors=True)
    #     # remove binaries
    #     for ext in ['', '.exe']:
    #         try:
    #             os.remove(
    #                 os.path.join(self.package_folder, 'bin',
    #                              'tesseract' + ext))
    #         except:
    #             pass

    # def package_info(self):
    #     self.cpp_info.libs = tools.collect_libs(self)
    #     if self.settings.os == "Linux":
    #         self.cpp_info.libs.extend(["pthread"])
    #     if self.settings.compiler == "Visual Studio":
    #         if not self.options.shared:
    #             self.cpp_info.libs.append('ws2_32')
