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
        else: # Linux and Darwin
            lib_name = "libCHILS.so"
            cc = "gcc"
            if platform.system() == "Darwin":
                try:
                    brew_prefix = subprocess.check_output(["brew", "--prefix", "gcc"], text=True).strip()
                    gcc_bin_dir = os.path.join(brew_prefix, "bin")
                    # Filter for actual compilers, e.g., gcc-15, not gcc-ranlib-15
                    compilers = sorted([f for f in os.listdir(gcc_bin_dir) if re.match(r'^gcc-\d+, f)])
                    if compilers:
                        cc = os.path.join(gcc_bin_dir, compilers[-1])
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Fallback to system gcc if brew command fails
                    pass
            make_command = ["make", f"CC={cc}", "-C", submodule_dir, lib_name]

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