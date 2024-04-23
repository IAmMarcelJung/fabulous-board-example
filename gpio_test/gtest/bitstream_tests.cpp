// tests.cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "fff.h"

#include <vector>

extern "C" {
#include <upload_bitstream.h>
#include <bitstream.h>
#include <gpio.h>
#include <gpio_mock.h>
}

#include <filesystem>
#include <iostream>

#define FFF_EMBEDED_CODE

DEFINE_FFF_GLOBALS;

#define FFF_FAKES_LIST(FAKE)    \
    FAKE(set_or_clear_gpio)      \
    FAKE(set_gpio)               \
    FAKE(clear_gpio)

class BitStreamTestSuite : public ::testing::Test
{
    protected:
        void SetUp() override
        {
            FFF_FAKES_LIST(RESET_FAKE);

            FFF_RESET_HISTORY();
            std::remove("transmitted_data.txt");
        }

        // Tear down common resources or state after each test case
        void TearDown() override {
            // Clean up common resources, teardown tasks, etc.
        }
};

template<typename T>

void print_arg_history(std::vector<T> history)
{
    std::cout << "History: " << std::endl;
//#for (T elem : history)
    for (size_t i = 0; i < history.size(); i += 2)
    {
        std::cout <<  static_cast<int>(history[i]) << ", ";
    }
    std::cout <<  std::endl;
}

TEST_F(BitStreamTestSuite, TestExampleBitstream)
{

    // Arrange
    uint8_t bitstream[] = {0x01, 0x02, 0x03, 0x0A};
    uint32_t bitstream_size = sizeof(bitstream)/sizeof(uint8_t);

    // Act
    upload_bitstream(bitstream, bitstream_size);

    bool * history_pointer = set_or_clear_pin_fake.arg2_history;

    // Assert
    ASSERT_EQ(set_or_clear_gpio_fake.call_count, 64);
    ASSERT_EQ(set_gpio_fake.call_count, 32);
    ASSERT_EQ(clear_gpio_fake.call_count, 32);
}

TEST_F(BitStreamTestSuite, TestBitstream)
{
    // Arrange
    uint32_t bitstream_size = sizeof(bitstream)/sizeof(uint8_t);
    set_or_clear_gpio_fake.custom_fake = my_fake;

    // Act
    upload_bitstream(bitstream, bitstream_size);
}
