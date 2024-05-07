include(CMakePrintHelpers)

cmake_print_variables(CMAKE_CURRENT_SOURCE_DIR)
add_executable(
  bitstream_tests
  bitstream_tests.cpp
  ${PROJECT_SOURCE_DIR}/firmware_helpers/upload_bitstream/upload_bitstream.c)
add_executable(gpio_tests gpio_tests.cpp
                          ${PROJECT_SOURCE_DIR}/firmware_helpers/gpio/gpio.c)
add_executable(
  register_tests
  register_tests.cpp
  ${PROJECT_SOURCE_DIR}/firmware_helpers/register_actions/register_actions.c)

add_custom_target(runTests DEPENDS bitstream_tests gpio_tests register_tests)

target_include_directories(
  bitstream_tests
  PRIVATE ${PROJECT_SOURCE_DIR}/firmware_helpers/upload_bitstream
          ${PROJECT_SOURCE_DIR}/firmware_helpers/bitstream
          ${PROJECT_SOURCE_DIR}/mocks/firmware_helpers_mock/inc
          ${PROJECT_SOURCE_DIR}/riscv_firmware_src
          ${PROJECT_SOURCE_DIR}/hw
          ${PROJECT_SOURCE_DIR}/gpio_config
          ${PROJECT_SOURCE_DIR}
          ${CMAKE_CURRENT_SOURCE_DIR})

target_include_directories(
  gpio_tests
  PRIVATE ${PROJECT_SOURCE_DIR}/firmware_helpers/gpio
          ${PROJECT_SOURCE_DIR}/riscv_firmware_src
          ${PROJECT_SOURCE_DIR}/hw
          ${PROJECT_SOURCE_DIR}/gpio_config
          ${PROJECT_SOURCE_DIR}/mocks/firmware_helpers_mock/inc
          ${PROJECT_SOURCE_DIR}
          ${CMAKE_CURRENT_SOURCE_DIR})

target_include_directories(
  register_tests PRIVATE ${PROJECT_SOURCE_DIR}/firmware_helpers/register_actions
                         ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(bitstream_tests PUBLIC gpio_mock upload_bitstream
                                             ${GTEST_LIBRARIES} gtest_main)

target_link_libraries(gpio_tests PUBLIC gpio ${GTEST_LIBRARIES} gtest_main
                                        register_actions_mock)
target_link_libraries(register_tests PUBLIC register_actions ${GTEST_LIBRARIES}
                                            gtest_main)

gtest_discover_tests(bitstream_tests)
gtest_discover_tests(gpio_tests)
gtest_discover_tests(register_tests)
