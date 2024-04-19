add_library(firmware_helpers_mock src/io_def_mock.c src/upload_bitstream_mock.c)

add_library(io_def_mock src/io_def_mock.c)
add_library(upload_bitstream_mock src/upload_bitstream_mock.c)

target_include_directories(
  firmware_helpers_mock
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc
         ${CMAKE_SOURCE_DIR}/firmware_helpers/upload_bitstream
         ${CMAKE_SOURCE_DIR}/gtest)

target_include_directories(
  io_def_mock
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc
         ${CMAKE_SOURCE_DIR}/firmware_helpers/io_def ${CMAKE_SOURCE_DIR}/gtest)

target_include_directories(
  upload_bitstream_mock
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc
         ${CMAKE_SOURCE_DIR}/firmware_helpers/upload_bitstream
         ${CMAKE_SOURCE_DIR}/gtest)

target_link_libraries(firmware_helpers_mock PUBLIC io_def upload_bitstream)
# target_link_libraries(io_def_mock PUBLIC io_def)
target_link_libraries(upload_bitstream_mock PUBLIC upload_bitstream)
