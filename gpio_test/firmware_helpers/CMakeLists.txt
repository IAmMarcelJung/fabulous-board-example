add_library(gpio STATIC gpio/gpio.c)
add_library(upload_bitstream STATIC upload_bitstream/upload_bitstream.c)
add_library(register_actions STATIC register_actions/register_actions.c)

target_include_directories(register_actions
                           PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/register_actions)

target_include_directories(
  gpio
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/gpio
         ${CMAKE_CURRENT_SOURCE_DIR}/register_actions ${CMAKE_SOURCE_DIR}/hw
         ${CMAKE_SOURCE_DIR}/riscv_firmware_src)

target_include_directories(
  upload_bitstream
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/upload_bitstream
         ${CMAKE_CURRENT_SOURCE_DIR}/gpio ${CMAKE_CURRENT_SOURCE_DIR}/bitstream
         ${CMAKE_SOURCE_DIR}/riscv_firmware_src)
