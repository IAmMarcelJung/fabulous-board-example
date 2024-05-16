// gpio_tests.cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>

extern "C" {
#include <gpio.h>
#include <register_actions_mock.h>
#include <defs.h>
#include <global_defs.h>
}
#include "fff.h"

#define FFF_EMBEDED_CODE

DEFINE_FFF_GLOBALS;

#define FFF_FAKES_LIST(FAKE)    \
    FAKE(set_or_clear_bit)

uint32_t datal_reg = 0u;
uint32_t datah_reg = 0u;
GPIO gpio;

class GpioTestSuite : public ::testing::Test
{
    protected:
        void SetUp() override
        {
            FFF_FAKES_LIST(RESET_FAKE)

            FFF_RESET_HISTORY();
            datal_reg = 0u;
            datah_reg = 0u;
            gpio.datal_reg_pointer = &datal_reg;
            gpio.datah_reg_pointer = &datah_reg;
            gpio_init(&gpio);
        }

        // Tear down common resources or state after each test case
        void TearDown() override {
            // Clean up common resources, teardown tasks, etc.
        }
};

uint8_t gpios[] =
{
    GPIO_0,
    GPIO_1,
    GPIO_2,
    GPIO_3,
    GPIO_4,
    GPIO_5,
    GPIO_6,
    GPIO_7,
    GPIO_8,
    GPIO_9,
    GPIO_10,
    GPIO_11,
    GPIO_12,
    GPIO_13,
    GPIO_14,
    GPIO_15,
    GPIO_16,
    GPIO_17,
    GPIO_18,
    GPIO_19,
    GPIO_20,
    GPIO_21,
    GPIO_22,
    GPIO_23,
    GPIO_24,
    GPIO_25,
    GPIO_26,
    GPIO_27,
    GPIO_28,
    GPIO_29,
    GPIO_30,
    GPIO_31,
    GPIO_32,
    GPIO_33,
    GPIO_34,
    GPIO_35,
    GPIO_36,
    GPIO_37,
};

#define GPIO_SCLK GPIO_36
#define GPIO_DATA GPIO_37

TEST_F(GpioTestSuite, TestSetGpio)
{
    for(uint8_t gpio = 0u; gpio < NUM_OF_GPIOS; gpio++)
    {
        // Arrange
        uint32_t expected_val = gpio % BITS_IN_WORD;
        volatile uint32_t * expected_reg = gpio < BITS_IN_WORD ? &reg_mprj_datal : &reg_mprj_datah;

        // Act
        set_gpio(gpio);

        // Assert
        ASSERT_EQ(set_bit_fake.arg0_val, expected_val);
    }
}

TEST_F(GpioTestSuite, TestClearGpio)
{
    for(uint8_t gpio = 0u; gpio < NUM_OF_GPIOS; gpio++)
    {
        // Arrange
        uint32_t expected_val = gpio % BITS_IN_WORD;

        // Act
        clear_gpio(gpio);

        // Assert
        ASSERT_EQ((uint32_t)clear_bit_fake.arg0_val, (uint32_t)expected_val);
    }
}

TEST_F(GpioTestSuite, TestSetOrClearGpio)
{
    for(uint8_t gpio = 0u; gpio < NUM_OF_GPIOS; gpio++)
    {
        // Arrange
        uint32_t expected_val = gpio % BITS_IN_WORD;
        volatile uint32_t * expected_reg = gpio < BITS_IN_WORD ? &reg_mprj_datal : &reg_mprj_datah;

        // Act
        set_or_clear_gpio(gpio, false);

        // Assert
        ASSERT_EQ(clear_bit_fake.arg0_val, expected_val);

        // Act
        set_or_clear_gpio(gpio, true);

        // Assert
        ASSERT_EQ(set_bit_fake.arg0_val, expected_val);
    }
}
