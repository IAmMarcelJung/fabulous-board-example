add_library(io_def STATIC io_def/io_def.c)
add_library(upload_bitstream STATIC upload_bitstream/upload_bitstream.c)

target_include_directories(
  io_def PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/io_def ${CMAKE_SOURCE_DIR}/hw
                ${CMAKE_SOURCE_DIR}/riscv_firmware_src)

target_include_directories(
  upload_bitstream
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/upload_bitstream
         ${CMAKE_CURRENT_SOURCE_DIR}/io_def
         ${CMAKE_CURRENT_SOURCE_DIR}/bitstream
         ${CMAKE_SOURCE_DIR}/riscv_firmware_src)
