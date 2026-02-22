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
        elif platform.system() == "Darwin": # macOS
            lib_name = "libCHILS.so"
            # Find homebrew gcc, as specified by the user
            try:
                proc = subprocess.run(
                    "find $(brew --prefix gcc)/bin -name 'gcc-*' | head -n 1",
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=True
                )
                cc = proc.stdout.strip()
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                # Fallback to default gcc if brew command fails
                print("Homebrew gcc not found, falling back to system gcc. This might fail.")
                print(e)
                cc = "gcc"
            
            make_command = ["make", "CC=" + cc, 'LDFLAGS="-static-libgomp"', "-C", submodule_dir, lib_name]
        else: # Linux
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
    version='1.0.1',
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