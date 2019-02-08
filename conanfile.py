from conans.model.conan_file import ConanFile
from conans import CMake

import os
import shutil
import distutils.dir_util

class WebRtcConan(ConanFile):
	name = "libwebrtc"
	version = "1.0.0"

	license = "MIT"
	author = "Steve White <steve.white@smoothwall.com>"
	
	url = "https://github.com/Smoothwall/libwebrtc"
	
	description = "Chromium webrtc packaged as a conan dependency"
	topics = ("webrtc")
		
	settings = {"os", "compiler", "arch", "build_type"}
	options = {"shared": [True, False]}
	generators = "cmake"
	exports_sources = "./*"
	 
	git_tag = version
	
	default_options = "shared=False"
	
	short_paths = True

	def source(self):
		print("INFO: tag: " + self.git_tag)
		
		#self.run("git clone --recurse-submodules -j6 --branch={0} --single-branch {1}.git .".format(self.git_tag, self.code_url)) 
		#self.run("git submodule update --init --recursive") 
		
	#def configure(self):
		#if self.settings.compiler == "Visual Studio":
		#	del self.settings.compiler.runtime
				
	def build(self):
		self.cmake = CMake(self)
		#self.definitions["CMAKE_BUILD_TYPE"] = self.settings.build_type
		
		print("INFO: Build: " + self.name + " - " + str(self.settings.os) + " - " + str(self.settings.build_type))
		print("INFO: src/build/cmdLine: " + self.source_folder + " - " + self.build_folder + " - " + self.cmake.command_line)

		print("INFO: Cmake configure")
		self.cmake.configure(source_folder=".")
		print("INFO: Cmake build")
		self.cmake.build()
	
	def package(self):
		# Package all dependencies in to a single package since we're statically compiling the client anyway.
		base = "."
		
		inc_dst_path = self.package_folder + "/include"
		
		libs = ['']
		
		for lib in libs:
			src_path = base + "/" + lib
			print("INFO: Copy headers: " + src_path + " -> " + inc_dst_path)
			distutils.dir_util.copy_tree(src_path, inc_dst_path)
			
		self.copy(pattern=base + '/deps/*.h', dst=inc_dst_path, keep_path=False)
		
		print("INFO: Copy libs")

		lib_dst_path = "lib"
		
		self.copy(pattern="*.lib", dst=lib_dst_path, keep_path=False)
		self.copy(pattern="*.dll", dst="bin", keep_path=False)
		self.copy(pattern="*.pdb", dst="bin", keep_path=False)

		self.copy(pattern="*.a", dst=lib_dst_path, keep_path=False)
		self.copy(pattern="*.so", dst=lib_dst_path, keep_path=False)
		self.copy(pattern="*.dylib", dst=lib_dst_path, keep_path=False)
		#self.copy(pattern="**/" + self.build_type + "/*.lib", dst=lib_dst_path, keep_path=False)

	def package_info(self):
		self.cpp_info.libs = ['']

		# In linux we need to link also with these libs
		if self.settings.os == "Linux":
			self.cpp_info.libs.extend(["pthread", "dl", "rt"])

		if not self.options.shared:
			if self.settings.compiler == "Visual Studio":
				self.cpp_info.libs.extend(["ws2_32", "Iphlpapi", "Crypt32", "Winhttp", "Ncrypt", "Rpcrt4", "Secur32"])
