# TCMalloc Conan package
# Dmitriy Vetutnev, ODANT 2018


from conans import ConanFile, MSBuild, tools
from conans.errors import ConanException
import os, glob


def get_safe(options, name):
    try:
        return getattr(options, name, None)
    except ConanException:
        return None


class FreeImageConan(ConanFile):
    name = "tcmalloc"
    version = "2.7.2000.1000"
    license = "BSD 3-Clause"
    description = "TCMalloc"
    url = "https://github.com/odant/conan-tcmalloc"
    settings = {
        "os": ["Windows"],
        "compiler": ["Visual Studio"],
        "build_type": ["Debug", "Release"],
        "arch": ["x86_64", "x86"]
    }
    options = {
        "dll_sign": [True, False]
    }
    default_options = "dll_sign=True"
    exports_sources = "src/*"
    no_copy_source = False
    build_policy = "missing"
    #
    commit = "9e5b1628737c67b4587f937164572774592978c4"

    def configure(self):
        # DLL sign
        if self.settings.os != "Windows":
            del self.options.dll_sign
        # Pure C library
        del self.settings.compiler.libcxx

    def build_requirements(self):
        if get_safe(self.options, "dll_sign"):
            self.build_requires("windows_signtool/[~=1.0]@%s/stable" % self.user)

    def build(self):
        if self.settings.compiler == "Visual Studio":
            self.msvc_build()

    def msvc_build(self):
        with tools.chdir("src"):
            builder = MSBuild(self)
            build_type = {
                "Release": "Release-Patch",
                "Debug": "Debug"
            }.get(str(self.settings.build_type))
            builder.build("gperftools.sln", upgrade_project=False, verbosity="normal", use_env=False, build_type=build_type, targets=["libtcmalloc_minimal"])

    def package(self):
        self.copy("tcmalloc64.lib", dst="lib", src="src/x64/Release-Patch", keep_path=False)
        self.copy("tcmalloc64.dll", dst="bin", src="src/x64/Release-Patch", keep_path=False)
        self.copy("tcmalloc64.pdb", dst="bin", src="src/x64/Release-Patch", keep_path=False)
        self.copy("tcmalloc64d.lib", dst="lib", src="src/x64/Debug", keep_path=False)
        self.copy("tcmalloc64d.dll", dst="bin", src="src/x64/Debug", keep_path=False)
        self.copy("tcmalloc64d.pdb", dst="bin", src="src/x64/Debug", keep_path=False)
        self.copy("tcmalloc.lib", dst="lib", src="src/Win32/Release-Patch", keep_path=False)
        self.copy("tcmalloc.dll", dst="bin", src="src/Win32/Release-Patch", keep_path=False)
        self.copy("tcmalloc.pdb", dst="bin", src="src/Win32/Release-Patch", keep_path=False)
        self.copy("tcmallocd.lib", dst="lib", src="src/Win32/Debug", keep_path=False)
        self.copy("tcmallocd.dll", dst="bin", src="src/Win32/Debug", keep_path=False)
        self.copy("tcmallocd.pdb", dst="bin", src="src/Win32/Debug", keep_path=False)
        # Sign DLL
        if get_safe(self.options, "dll_sign"):
            import windows_signtool
            pattern = os.path.join(self.package_folder, "bin", "*.dll")
            for fpath in glob.glob(pattern):
                fpath = fpath.replace("\\", "/")
                for alg in ["sha1", "sha256"]:
                    is_timestamp = True if self.settings.build_type == "Release" else False
                    cmd = windows_signtool.get_sign_command(fpath, digest_algorithm=alg, timestamp=is_timestamp)
                    self.output.info("Sign %s" % fpath)
                    self.run(cmd)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
