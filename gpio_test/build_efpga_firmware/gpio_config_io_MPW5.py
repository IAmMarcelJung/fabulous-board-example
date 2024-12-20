# number of IO in the configuration stream for each chain
NUM_IO = 19

# defines these values for IO configurations
C_MGMT_OUT = 0
C_MGMT_IN = 1
C_USER_BIDIR = 2
C_DISABLE = 3
C_ALL_ONES = 4
C_USER_BIDIR_WPU = 5
C_USER_BIDIR_WPD = 6
C_USER_IN_NOPULL = 7
C_USER_OUT = 8
C_MGMT_HIGH_Z_STRONG_0_DISABLE_OUTPUT = 9
C_MGMT_HIGH_Z_STRONG_0 = 10

config_h = [
    C_USER_BIDIR_WPU,  # 37
    C_USER_BIDIR_WPU,  # 36
    C_USER_BIDIR_WPU,  # 35
    C_USER_BIDIR_WPU,  # 34
    C_USER_BIDIR_WPU,  # 33
    C_USER_BIDIR_WPU,  # 32
    C_USER_BIDIR_WPU,  # 31
    C_USER_BIDIR_WPU,  # 30
    C_USER_BIDIR_WPU,  # 29
    C_USER_BIDIR_WPU,  # 28
    C_USER_BIDIR_WPU,  # 27
    C_DISABLE,  # 26
    C_USER_BIDIR_WPU,  # 25
    C_DISABLE,  # 24
    C_USER_BIDIR_WPU,  # 23
    C_DISABLE,  # 22
    C_USER_BIDIR_WPU,  # 21
    C_DISABLE,  # 20
    C_DISABLE,  # 19
]

del config_h[NUM_IO:]

config_l = [
    C_ALL_ONES,  # 0
    C_MGMT_OUT,  # 1
    C_MGMT_IN,  # 2
    C_MGMT_IN,  # 3
    C_MGMT_IN,  # 4
    C_ALL_ONES,  # 5
    C_ALL_ONES,  # 6
    C_MGMT_HIGH_Z_STRONG_0_DISABLE_OUTPUT,  # 7
    C_MGMT_HIGH_Z_STRONG_0_DISABLE_OUTPUT,  # 8
    C_MGMT_HIGH_Z_STRONG_0_DISABLE_OUTPUT,  # 9
    C_ALL_ONES,  # 10
    C_MGMT_HIGH_Z_STRONG_0,  # 11
    C_MGMT_HIGH_Z_STRONG_0,  # 12
    C_MGMT_HIGH_Z_STRONG_0,  # 13
    C_DISABLE,  # 14
    C_USER_BIDIR_WPU,  # 15
    C_DISABLE,  # 16
    C_USER_BIDIR_WPU,  # 17
    C_DISABLE,  # 18
]

del config_l[NUM_IO:]
