import os
import re
import subprocess
import platform
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

class CustomBuild(build_py):
    def run(self):
        submodule_dir = "CHILS"
        # Determine the library name based on the OS
        if platform.system() == "Windows":
            lib_name = "libCHILS.dll"
            make_command = ["make", "CC=gcc", "-C", submodule_dir, lib_name]
        else: # Linux or macOS
            lib_name = "libCHILS.so"
            cc = "gcc"
            make_command = ["make", "CC=" + cc, "-C", submodule_dir, lib_name]

        # Build the library inside the submodule directory
        subprocess.check_call(make_command)

        # The target directory for the library is inside the build folder
        target_dir = os.path.join(self.build_lib, "chils")
        self.mkpath(target_dir)
        
        # The source library is in the submodule directory
        source_lib = os.path.join(submodule_dir, lib_name)
        self.copy_file(source_lib, os.path.join(target_dir, lib_name))

        super().run()


setup(
    name='chils',
    version='1.0.0',
    author='Kenneth Langedal',
    packages=find_packages(where="python"),
    package_dir={"" : "python"},
    cmdclass={
        'build_py': CustomBuild,
    },
    package_data={
        'chils': ['*.so', '*.dll'],
    },
    include_package_data=True,
    has_ext_modules=lambda : True
)