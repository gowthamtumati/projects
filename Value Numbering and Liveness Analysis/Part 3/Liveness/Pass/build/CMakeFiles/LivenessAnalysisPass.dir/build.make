# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/gowtham/Downloads/Liveness/Pass/Transforms/LivenessAnalysis

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/gowtham/Downloads/Liveness/Pass/build

# Include any dependencies generated for this target.
include CMakeFiles/LivenessAnalysisPass.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/LivenessAnalysisPass.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/LivenessAnalysisPass.dir/flags.make

CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o: CMakeFiles/LivenessAnalysisPass.dir/flags.make
CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o: /home/gowtham/Downloads/Liveness/Pass/Transforms/LivenessAnalysis/LivenessAnalysis.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gowtham/Downloads/Liveness/Pass/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o -c /home/gowtham/Downloads/Liveness/Pass/Transforms/LivenessAnalysis/LivenessAnalysis.cpp

CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/gowtham/Downloads/Liveness/Pass/Transforms/LivenessAnalysis/LivenessAnalysis.cpp > CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.i

CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/gowtham/Downloads/Liveness/Pass/Transforms/LivenessAnalysis/LivenessAnalysis.cpp -o CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.s

CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o.requires:

.PHONY : CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o.requires

CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o.provides: CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o.requires
	$(MAKE) -f CMakeFiles/LivenessAnalysisPass.dir/build.make CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o.provides.build
.PHONY : CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o.provides

CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o.provides.build: CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o


# Object files for target LivenessAnalysisPass
LivenessAnalysisPass_OBJECTS = \
"CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o"

# External object files for target LivenessAnalysisPass
LivenessAnalysisPass_EXTERNAL_OBJECTS =

libLivenessAnalysisPass.so: CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o
libLivenessAnalysisPass.so: CMakeFiles/LivenessAnalysisPass.dir/build.make
libLivenessAnalysisPass.so: CMakeFiles/LivenessAnalysisPass.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/gowtham/Downloads/Liveness/Pass/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared module libLivenessAnalysisPass.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/LivenessAnalysisPass.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/LivenessAnalysisPass.dir/build: libLivenessAnalysisPass.so

.PHONY : CMakeFiles/LivenessAnalysisPass.dir/build

CMakeFiles/LivenessAnalysisPass.dir/requires: CMakeFiles/LivenessAnalysisPass.dir/LivenessAnalysis.cpp.o.requires

.PHONY : CMakeFiles/LivenessAnalysisPass.dir/requires

CMakeFiles/LivenessAnalysisPass.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/LivenessAnalysisPass.dir/cmake_clean.cmake
.PHONY : CMakeFiles/LivenessAnalysisPass.dir/clean

CMakeFiles/LivenessAnalysisPass.dir/depend:
	cd /home/gowtham/Downloads/Liveness/Pass/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/gowtham/Downloads/Liveness/Pass/Transforms/LivenessAnalysis /home/gowtham/Downloads/Liveness/Pass/Transforms/LivenessAnalysis /home/gowtham/Downloads/Liveness/Pass/build /home/gowtham/Downloads/Liveness/Pass/build /home/gowtham/Downloads/Liveness/Pass/build/CMakeFiles/LivenessAnalysisPass.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/LivenessAnalysisPass.dir/depend

