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

find_package(GTest)
include(GoogleTest)

add_subdirectory(firmware_helpers)
add_subdirectory(gtest)
add_subdirectory(mocks)
add_subdirectory(riscv_firmware_src)
add_subdirectory(gpio_config)
