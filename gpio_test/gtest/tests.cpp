// tests.cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "fff.h"

#include <upload_bitstream.h>
#include <bitstream.h>
#include <io_def_mock.h>

#define FFF_EMBEDED_CODE

DEFINE_FFF_GLOBALS;

#define FFF_FAKES_LIST(FAKE)    \
    FAKE(set_or_clear)          \
    FAKE(set_pin)               \
    FAKE(clear_pin)

class MyTestSuite : public ::testing::Test
{
    protected:
        void SetUp() override
        {
            FFF_FAKES_LIST(RESET_FAKE);

            FFF_RESET_HISTORY();
        }

        // Tear down common resources or state after each test case
        void TearDown() override {
            // Clean up common resources, teardown tasks, etc.
        }
};

TEST(UploadBitstreamTest, TestCall) {
    uint8_t bitstream[] = {0x01, 0x02, 0x03, 0x0A};
    //upload_bitstream(bitstream, sizeof(bitstream)/sizeof(uint8_t));
    upload_bitstream(bitstream, sizeof(bitstream)/sizeof(uint8_t));
    ASSERT_EQ(set_or_clear_fake.call_count, 2);
    //ASSERT_EQ(set_pin_fake.call_count, 1);
    //ASSERT_EQ(0, squareRoot(0.0));
}
