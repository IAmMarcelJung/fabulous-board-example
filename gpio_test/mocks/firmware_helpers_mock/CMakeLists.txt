add_library(firmware_helpers_mock
    src/io_def_mock.c
    src/upload_bitstream_mock.c
    )

target_include_directories(firmware_helpers_mock PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/inc
    ${CMAKE_SOURCE_DIR}/firmware_helpers/include
    ${CMAKE_SOURCE_DIR}/gtest
    )

target_link_libraries(firmware_helpers_mock PUBLIC
    firmware_helpers
    )
