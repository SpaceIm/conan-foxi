from conans import ConanFile, CMake, tools
import glob
import os


class FoxiConan(ConanFile):
    name = "foxi"
    description = "ONNXIFI with Facebook Extension."
    license = "MIT"
    topics = ("conan", "foxi", "onnxifi")
    homepage = "https://github.com/houseroad/foxi"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    exports_sources = ["CMakeLists.txt", "patches/**"]
    generators = "cmake"
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = glob.glob("foxi-*")[0]
        os.rename(extracted_dir, self._source_subfolder)

    def _patch_sources(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"),
                              "DESTINATION lib",
                              "RUNTIME DESTINATION bin ARCHIVE DESTINATION lib LIBRARY DESTINATION lib")

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["FOXI_WERROR"] = False
        self._cmake.configure()
        return self._cmake

    def build(self):
        self._patch_sources()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["foxi_dummy", "foxi_loader"]
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["dl"]
