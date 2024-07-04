// tests.cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "fff.h"

extern "C" {
#include <upload_bitstream.h>
#include <bitstream.h>
#include <global_defs.h>
#include <gpio.h>
#include <gpio_mock.h>
#include <gpio_config_io_mock.h>
}

#include <iostream>

#define FFF_EMBEDED_CODE

DEFINE_FFF_GLOBALS;

#define FFF_FAKES_LIST(FAKE) \
    FAKE(set_or_clear_gpio) \
    FAKE(set_gpio) \
    FAKE(clear_gpio) \
    FAKE(delay)
volatile uint32_t datal_reg;
volatile uint32_t datah_reg;


GPIO gpio;

class BitStreamTestSuite : public ::testing::Test
{
    protected:
        void SetUp() override
        {
            FFF_FAKES_LIST(RESET_FAKE);

            FFF_RESET_HISTORY();
            gpio.datah_reg_pointer = &datah_reg;
            gpio.datal_reg_pointer = &datal_reg;
            bitstream_init(&gpio);
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
    for (size_t i = 0; i < history.size(); i += 2)
    {
        std::cout <<  static_cast<int>(history[i]) << ", ";
    }
    std::cout <<  std::endl;
}

#define CTRL_WORD_ENABLE_BITBANG 0x0000FAB1u

TEST_F(BitStreamTestSuite, TestExampleBitstream)
{

    // Arrange
    uint8_t test_bitstream[] = {0x01, 0x02, 0x03, 0x0A};
    // 00000001 00000010 00000011 00001010
    uint32_t bitstream_size = sizeof(test_bitstream)/sizeof(uint8_t);
    bitstream_init(&gpio);

    // Act
    upload_bitstream(test_bitstream, bitstream_size);

    // Assert
    ASSERT_EQ(set_or_clear_gpio_fake.call_count, 64);
    ASSERT_EQ(clear_gpio_fake.call_count, 32);
    ASSERT_EQ(set_gpio_fake.call_count, 32);
    uint8_t loop_counter = 0u;
    for (uint8_t byte = 0u; byte < FFF_ARG_HISTORY_LEN; byte++)
    {
        for (uint8_t bit = 0u; bit < BITS_IN_BYTE;  bit++)
        {
            for (uint8_t j = 0u; j < 2; j++)
            {
                bool bitstream_value;
                uint8_t control_word_bit_pos = MSB_IN_WORD - loop_counter/2 ;
                bool history_value = set_or_clear_gpio_fake.arg1_history[loop_counter];

                // bistream data
                if (j == 0)
                {
                    bitstream_value = (test_bitstream[byte] >> (MSB_IN_BYTE - bit)) & 1u;
                }
                // control word data
                else
                {
                    bitstream_value = (CTRL_WORD_ENABLE_BITBANG >> control_word_bit_pos) & 1u;
                }
                if (j == 0)
                {
                    std::cout << "RISING_EDGE " << ": History: " << history_value << ", bitstream value: " << bitstream_value << std::endl;
                }
                else
                {
                    std::cout << "FALLING_EDGE" <<  ": History: " << history_value << ", bitstream value: " << bitstream_value << std::endl;
                }
                loop_counter++;
                EXPECT_EQ(history_value, bitstream_value);

            }
        }
    }
}

TEST_F(BitStreamTestSuite, TestBitstream)
{
    GTEST_SKIP() << "This is only needed to write out a bitstream file and compare it to a known good.";

    // Arrange
    std::remove("transmitted_data.txt");
    uint32_t bitstream_size = sizeof(bitstream)/sizeof(uint8_t);
    set_or_clear_gpio_fake.custom_fake = write_bit_to_file;
    set_gpio_fake.custom_fake = write_newline_to_file;

    // Act
    upload_bitstream(bitstream, bitstream_size);

    // Assert
    // TODO: compare the produced bitstream with the bitstream produced by the simulation
}
