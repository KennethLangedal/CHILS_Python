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
            os.environ.setdefault("MACOSX_DEPLOYMENT_TARGET", "11.0")

            lib_name = "libCHILS.so"

            llvm_prefix = subprocess.check_output(
                ["brew", "--prefix", "llvm"], text=True
            ).strip()

            cc = os.path.join(llvm_prefix, "bin", "clang")

            libomp_root = os.environ.get("LIBOMP_ROOT")
            if not libomp_root:
                raise RuntimeError(
                    "LIBOMP_ROOT not set. libomp must be built in CI."
                )

            include_dir = os.path.join(libomp_root, "include")
            dylib_path  = os.path.join(libomp_root, "lib")

            cflags = [
                "-Xpreprocessor",
                f"-I{include_dir}",
            ]

            ldflags = [
                f"-L{lib_path}",
                "-lomp",
                "-Wl,-rpath,@loader_path/.dylibs",
            ]

            make_command = [
                "make",
                f"CC={cc}",
                f"CFLAGS={' '.join(cflags)}",
                f"LDFLAGS={' '.join(ldflags)}",
                "-C", submodule_dir,
                lib_name,
            ]
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