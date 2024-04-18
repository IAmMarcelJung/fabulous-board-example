cmake_minimum_required(VERSION 3.25 FATAL_ERROR)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# Print the contents of the INCLUDE_DIRECTORIES variable
include(CMakePrintHelpers)
cmake_print_variables(INCLUDE_DIRECTORIES)
add_compile_definitions(GTEST)



set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
project(caravel_firmware)
cmake_print_variables(C_MAKE_CXX_COMPILER)

include(FetchContent)
FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/f8d7d77c06936315286eb55f8de22cd23c188571.zip
)

FetchContent_MakeAvailable(googletest)

enable_testing()
#[===[
add_executable(
    hello_test
    hello_test.cc
    )
target_link_libraries(
    hello_test
    GTest::gtest_main
    )
]===]

find_package(GTest)
include(GoogleTest)
#gtest_discover_tests(hello_test)
#add_custom_target(build_runTests
#    COMMAND ${CMAKE_COMMAND} --build ${CMAKE_BINARY_DIR} --target runTests
#    COMMENT "Building runTests"
#)

#add_dependencies(build_runTests runTests)
#

add_subdirectory(firmware_helpers)
add_subdirectory(gtest)
add_subdirectory(mocks)
add_subdirectory(riscv_firmware_src)
add_subdirectory(gpio_config)

#include_directories(riscv_firmware_src)
#include_directories(generated)
#include_directories(hw)
#include_directories(gtest)
#include_directories(mocks)
#include_directories(firmware_helpers)
