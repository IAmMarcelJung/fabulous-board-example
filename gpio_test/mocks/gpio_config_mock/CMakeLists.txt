add_library(gpio_config_mock src/gpio_config_data_mock.c
                             src/gpio_config_io_mock.c)

target_include_directories(
  gpio_config_mock
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc ${CMAKE_SOURCE_DIR}/gpio_config/
         ${CMAKE_SOURCE_DIR}/gtest)

target_link_libraries(gpio_config_mock PUBLIC gpio_config)
