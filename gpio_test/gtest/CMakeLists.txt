#find_package(GTest REQUIRED)
include(CMakePrintHelpers)

cmake_print_variables(CMAKE_CURRENT_SOURCE_DIR)
add_executable(runTests
    tests.cpp
    )

add_compile_definitions(GTEST)

target_include_directories(runTests PRIVATE
    ${PROJECT_SOURCE_DIR}/firmware_helpers/inc
    ${PROJECT_SOURCE_DIR}/mocks/firmware_helpers_mock/inc
    ${PROJECT_SOURCE_DIR}/riscv_firmware_src
    ${PROJECT_SOURCE_DIR}/hw
    ${PROJECT_SOURCE_DIR}/gpio_config
    ${PROJECT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR})
#target_include_directories(runTests PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
#target_link_libraries(runTests ${GTEST_LIBRARIES}  gtest gtest_main firmware_helpers firmware_helpers_mock)
target_link_libraries(runTests PUBLIC
    firmware_helpers
    firmware_helpers_mock
    ${GTEST_LIBRARIES}
    gtest_main
    )
#target_link_libraries(runTests ${GTEST_LIBRARIES} firmware_helpers/include firmware_helpers_mock)

gtest_discover_tests(runTests)
