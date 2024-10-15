/* Redefine the bit patterns for the configuration words */

#define GPIO_MODE_MGMT_STD_INPUT_NOPULL 0x1003
#define GPIO_MODE_MGMT_STD_OUTPUT 0x1801
#define GPIO_MODE_MGMT_STD_ANALOG 0x100b

#define GPIO_MODE_USER_STD_INPUT_NOPULL 0x0402
#define GPIO_MODE_USER_STD_OUTPUT 0x0c00
#define GPIO_MODE_USER_STD_ANALOG 0x0000

/* Redefine the bit patterns that should *not* be used so that  */
/* they will force an error at compile time.                    */

#define GPIO_MODE_MGMT_STD_INPUT_PULLDOWN ERROR
#define GPIO_MODE_MGMT_STD_INPUT_PULLUP ERROR
#define GPIO_MODE_MGMT_STD_BIDIRECTIONAL ERROR

#define GPIO_MODE_USER_STD_INPUT_PULLDOWN ERROR
#define GPIO_MODE_USER_STD_INPUT_PULLUP ERROR
#define GPIO_MODE_USER_STD_BIDIRECTIONAL ERROR
#define GPIO_MODE_USER_STD_OUT_MONITORED ERROR
