add_library(firmware_helpers_mock src/gpio_mock.c src/upload_bitstream_mock.c
                                  src/register_actions_mock.c)

add_library(register_actions_mock src/register_actions_mock.c)
add_library(gpio_mock src/gpio_mock.c)
add_library(upload_bitstream_mock src/upload_bitstream_mock.c)

target_include_directories(
  firmware_helpers_mock
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc
         ${CMAKE_SOURCE_DIR}/firmware_helpers/upload_bitstream
         ${CMAKE_SOURCE_DIR}/gtest)

target_include_directories(
  register_actions_mock
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc
         ${CMAKE_SOURCE_DIR}/firmware_helpers/register_actions_mock
         ${CMAKE_SOURCE_DIR}/gtest)

target_include_directories(
  gpio_mock
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc
         ${CMAKE_SOURCE_DIR}/firmware_helpers/gpio ${CMAKE_SOURCE_DIR}/gtest)

target_include_directories(
  upload_bitstream_mock
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc
         ${CMAKE_SOURCE_DIR}/firmware_helpers/upload_bitstream
         ${CMAKE_SOURCE_DIR}/gtest)

target_link_libraries(firmware_helpers_mock PUBLIC register_actions gpio
                                                   upload_bitstream)
target_link_libraries(upload_bitstream_mock PUBLIC upload_bitstream)
target_link_libraries(register_actions_mock PUBLIC register_actions)
