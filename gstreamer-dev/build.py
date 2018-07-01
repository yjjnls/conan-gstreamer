#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_template_default
import os
import platform

if __name__ == "__main__":
    CONAN_USERNAME = os.environ.get("CONAN_USERNAME", "yjjnls")
    CONAN_UPLOAD = 'https://api.bintray.com/conan/%s/%s' % (CONAN_USERNAME,
                                                            'stable')
    os.environ['CONAN_UPLOAD'] = CONAN_UPLOAD
    os.environ['CONAN_CHANNEL'] = 'stable'
    os.environ['CONAN_UPLOAD_ONLY_WHEN_STABLE'] = 'False'
    os.environ['CONAN_USERNAME'] = CONAN_USERNAME

    builder = build_template_default.get_builder()
    builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:
        # dynamic only
        if not options["gstreamer-dev:shared"]:
            continue
        # release only
        if settings["build_type"] == "Debug":
            continue

        # Visual Sutido 2017 only
        if platform.system() == "Windows":
            if settings["compiler"] == "Visual Studio":
                if settings["compiler.version"] == '14':
                    builds.append(
                        [settings, options, env_vars, build_requires])
        elif platform.system() == "Linux":
            if settings["compiler"] == "gcc":
                if settings["compiler.version"] == '4.9' and settings["arch"] == 'x86_64':
                    builds.append(
                        [settings, options, env_vars, build_requires])
    builder.builds = builds

    builder.run()
