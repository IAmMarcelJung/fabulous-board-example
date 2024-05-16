// gpio_tests.cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>

extern "C" {
#include <register_actions.h>
}

class RegisterTestSuite : public ::testing::Test
{
    protected:
        void SetUp() override
        {
        }

        void TearDown() override {
        }
};

uint8_t defintions[] = {
    REGISTER_0_DATA_BIT_POS,
    REGISTER_1_DATA_BIT_POS,
    REGISTER_2_DATA_BIT_POS,
    REGISTER_3_DATA_BIT_POS,
    REGISTER_4_DATA_BIT_POS,
    REGISTER_5_DATA_BIT_POS,
    REGISTER_6_DATA_BIT_POS,
    REGISTER_7_DATA_BIT_POS,
    REGISTER_8_DATA_BIT_POS,
    REGISTER_9_DATA_BIT_POS,
    REGISTER_10_DATA_BIT_POS,
    REGISTER_11_DATA_BIT_POS,
    REGISTER_12_DATA_BIT_POS,
    REGISTER_13_DATA_BIT_POS,
    REGISTER_14_DATA_BIT_POS,
    REGISTER_15_DATA_BIT_POS,
    REGISTER_16_DATA_BIT_POS,
    REGISTER_17_DATA_BIT_POS,
    REGISTER_18_DATA_BIT_POS,
    REGISTER_19_DATA_BIT_POS,
    REGISTER_20_DATA_BIT_POS,
    REGISTER_21_DATA_BIT_POS,
    REGISTER_22_DATA_BIT_POS,
    REGISTER_23_DATA_BIT_POS,
    REGISTER_24_DATA_BIT_POS,
    REGISTER_25_DATA_BIT_POS,
    REGISTER_26_DATA_BIT_POS,
    REGISTER_27_DATA_BIT_POS,
    REGISTER_28_DATA_BIT_POS,
    REGISTER_29_DATA_BIT_POS,
    REGISTER_30_DATA_BIT_POS,
    REGISTER_31_DATA_BIT_POS,
};

TEST_F(RegisterTestSuite, TestSetAllBits)
{
    // Arrange
    uint32_t test_reg = 0u;

    for (uint32_t i = 0u; i <= 31u; i++)
    {
        test_reg = 0u;
        // Act
        set_bit(defintions[i], &test_reg);
        // Assert
        ASSERT_EQ(test_reg, 1u << i);
    }
}

TEST_F(RegisterTestSuite, TestClearAllBits)
{
    // Arrange
    uint32_t test_reg = 0u;

    for (uint32_t i = 0u; i <= 31u; i++)
    {
        test_reg = 0xFFFFFFFFu;
        // Act
        clear_bit(defintions[i], &test_reg);
        uint32_t bit_mask =  0xFFFFFFFFu & ~(1u << i);
        // Assert
        ASSERT_EQ(test_reg, bit_mask);
    }
}

TEST_F(RegisterTestSuite, TestSetOrClearBitClearAllBits)
{
    // Arrange
    uint32_t test_reg = 0u;

    for (uint32_t i = 0u; i <= 31u; i++)
    {
        test_reg = 0xFFFFFFFFu;
        // Act
        set_or_clear_bit(defintions[i], &test_reg, false);
        uint32_t bit_mask =  0xFFFFFFFFu & ~(1u << i);
        // Assert
        ASSERT_EQ(test_reg, bit_mask);
    }
}

TEST_F(RegisterTestSuite, TestSetOrClearBitSetAllBits)
{
    // Arrange
    uint32_t test_reg = 0u;

    for (uint32_t i = 0u; i <= 31u; i++)
    {
        test_reg = 0x0;
        // Act
        set_or_clear_bit(defintions[i], &test_reg, true);
        // Assert
        ASSERT_EQ(test_reg, 1u << i);
    }
}


TEST_F(RegisterTestSuite, TestClearOnlyOneBit)
{
    // Arrange
    uint32_t test_reg = 0xFFFFFFFFu;

    // Act
    clear_bit(REGISTER_31_DATA_BIT_POS, &test_reg);

    // Assert
    ASSERT_EQ(0x7FFFFFFFu, test_reg);
}

TEST_F(RegisterTestSuite, TestSequence)
{

    // Arrange
    uint32_t test_reg = 0u;

    // Act - set data register
    set_bit(REGISTER_5_DATA_BIT_POS, &test_reg);

    // Assert
    ASSERT_EQ(1u << 5u, test_reg);

    // Act - set clock register
    set_bit(REGISTER_4_DATA_BIT_POS, &test_reg);

    // Assert
    ASSERT_EQ(3u << 4u, test_reg);

    // Act - set data register
    set_bit(REGISTER_5_DATA_BIT_POS, &test_reg);

    // Assert
    ASSERT_EQ(3u << 4u, test_reg);

    // Act - clear clock register
    clear_bit(REGISTER_4_DATA_BIT_POS, &test_reg);

    // Assert
    ASSERT_EQ(1u << 5u, test_reg);
}
