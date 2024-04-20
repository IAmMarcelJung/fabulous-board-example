// tests.cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "fff.h"

#include <vector>

extern "C" {
#include <upload_bitstream.h>
#include <bitstream.h>
#include <io_def.h>
#include <io_def_mock.h>
}

#include <filesystem>
#include <iostream>

#define FFF_EMBEDED_CODE

DEFINE_FFF_GLOBALS;

#define FFF_FAKES_LIST(FAKE)    \
    FAKE(set_or_clear_pin)      \
    FAKE(set_pin)               \
    FAKE(clear_pin)

class BitStreamTestSuite : public ::testing::Test
{
    protected:
        void SetUp() override
        {
            FFF_FAKES_LIST(RESET_FAKE);

            FFF_RESET_HISTORY();
            set_or_clear_pin_fake.custom_fake = my_fake;
            ASSERT_EQ(std::remove("transmitted_data.txt"), 0) << "Could not remove transmitted data file." << std::endl;
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

TEST_F(BitStreamTestSuite, TestCall)
{

    uint8_t bitstream[] = {0x01, 0x02, 0x03, 0x0A};
    uint32_t bitstream_size = sizeof(bitstream)/sizeof(uint8_t);
    std::cout << "bitstream_size: " <<  bitstream_size << std::endl;
    upload_bitstream(bitstream, bitstream_size);

    bool * history_pointer = set_or_clear_pin_fake.arg2_history;
    std:std::vector<uint8_t> history(history_pointer, history_pointer + 50);
    print_arg_history(history);
    ASSERT_EQ(set_or_clear_pin_fake.call_count, 64);
    ASSERT_EQ(set_pin_fake.call_count, 32);
    ASSERT_EQ(clear_pin_fake.call_count, 32);
}

TEST_F(BitStreamTestSuite, TestBitstream)
{
    uint32_t bitstream_size = sizeof(bitstream)/sizeof(uint8_t);
    upload_bitstream(bitstream, bitstream_size);
}
