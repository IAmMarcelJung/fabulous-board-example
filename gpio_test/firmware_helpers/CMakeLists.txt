add_library(firmware_helpers STATIC
    src/io_def.c
    src/upload_bitstream.c)

target_include_directories(firmware_helpers PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/inc
    ${CMAKE_SOURCE_DIR}/riscv_firmware_src
)
