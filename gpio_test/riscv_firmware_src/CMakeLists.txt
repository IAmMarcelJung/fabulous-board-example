add_library(riscv_firmware isr.c stub.c print_io.c crt0_vex.S)

target_include_directories(
  riscv_firmware PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_SOURCE_DIR}/hw
                        ${CMAKE_SOURCE_DIR})
