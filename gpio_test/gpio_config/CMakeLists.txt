add_library(gpio_config gpio_config_io.c)

target_include_directories(
  gpio_config
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_SOURCE_DIR} ${CMAKE_SOURCE_DIR}/hw
         ${CMAKE_SOURCE_DIR}/riscv_firmware_src)
