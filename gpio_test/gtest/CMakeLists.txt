# find_package(GTest REQUIRED)
include(CMakePrintHelpers)

cmake_print_variables(CMAKE_CURRENT_SOURCE_DIR)
add_executable(runTests bitstream_tests.cpp)

add_compile_definitions(GTEST)

target_include_directories(
  runTests
  PRIVATE ${PROJECT_SOURCE_DIR}/firmware_helpers/upload_bitstream
          ${PROJECT_SOURCE_DIR}/firmware_helpers/bitstream
          ${PROJECT_SOURCE_DIR}/mocks/firmware_helpers_mock/inc
          ${PROJECT_SOURCE_DIR}/riscv_firmware_src
          ${PROJECT_SOURCE_DIR}/hw
          ${PROJECT_SOURCE_DIR}/gpio_config
          ${PROJECT_SOURCE_DIR}
          ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(runTests PUBLIC io_def_mock upload_bitstream
                                      ${GTEST_LIBRARIES} gtest_main)

gtest_discover_tests(runTests)
