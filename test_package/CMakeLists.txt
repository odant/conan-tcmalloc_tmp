project(PackageTest CXX)
cmake_minimum_required(VERSION 3.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

enable_testing()


#add_executable(binary_trees binary_trees.cc)
#target_link_libraries(binary_trees CONAN_PKG::tcmalloc)
#set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /INCLUDE:__tcmalloc")
#add_test(
#    NAME binary_trees
#    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#    COMMAND binary_trees
#)

add_executable(test_package test_package.cpp)
target_link_libraries(test_package CONAN_PKG::tcmalloc)
set_property(TARGET test_package PROPERTY LINK_FLAGS "/INCLUDE:__tcmalloc")
add_test(
    NAME test_package
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND test_package
)
