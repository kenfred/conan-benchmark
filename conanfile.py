from conans import ConanFile, CMake, tools
import shutil
import os, sys

class BenchmarkConan(ConanFile):
    name = "benchmark"
    version = "1.2.0"
    license = "Apache License Version 2.0"
    url = "http://github.com/kenfred/conan_benchmark"
    repo_url = 'https://github.com/google/benchmark.git'
    description = "A library to support the benchmarking of functions, similar to unit-tests."
    settings = "os", "compiler", "build_type", "arch"
    options = { "shared": [True, False], 
                "enable_testing": [True, False],
                "enable_exceptions": [True, False],
                "enable_lto": [True, False],
                "use_libcxx": [True, False]}
    default_options = "shared=False", "enable_testing=True", "enable_exceptions=True", "enable_lto=False", "use_libcxx=False"    
    _source_dir = "benchmark-%s" % version

    def source(self):
        file_name = "v%s.zip" % self.version if sys.platform == "win32" else "v%s.tar.gz" % self.version
        zip_name = "benchmark-%s.zip" % self.version if sys.platform == "win32" else "benchmark-%s.tar.gz" % self.version
        url = "https://github.com/google/benchmark/archive/%s" % file_name
        self.output.info("Downloading %s..." % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self)

        defs = dict()
        defs['CMAKE_INSTALL_PREFIX'] = self.package_folder
        defs['BENCHMARK_ENABLE_TESTING'] = "ON" if self.options.enable_testing else "OFF"
        defs['BENCHMARK_ENABLE_EXCEPTIONS'] = "ON" if self.options.enable_exceptions else "OFF"
        defs['BENCHMARK_ENABLE_LTO'] = "ON" if self.options.enable_lto else "OFF"
        defs['BENCHMARK_USE_LIBCXX'] = "ON" if self.options.use_libcxx else "OFF"
        defs['BENCHMARK_BUILD_32_BITS'] = "ON" if (self.settings.arch=="x86" and self.settings.compiler=="gcc") else "OFF"
            
        cmake.configure(source_dir=self._source_dir, build_dir=".", defs=defs)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src="benchmark")
        self.copy("*benchmark.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["benchmark"]
        self.cpp_info.includedirs = ["include"]

