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
    C_USER_BIDIR_WPU,  # 26
    C_USER_BIDIR_WPU,  # 25
    C_USER_BIDIR_WPU,  # 24
    C_USER_BIDIR_WPU,  # 23
    C_USER_BIDIR_WPU,  # 22
    C_USER_BIDIR_WPU,  # 21
    C_USER_BIDIR_WPU,  # 20
    C_USER_BIDIR_WPU,  # 19
]

del config_h[NUM_IO:]

config_l = [
    C_ALL_ONES,  # 0
    C_MGMT_OUT,  # 1
    C_MGMT_IN,  # 2
    C_MGMT_IN,  # 3
    C_MGMT_IN,  # 4
    C_MGMT_IN,  # 5
    C_MGMT_OUT,  # 6
    C_USER_BIDIR_WPU,  # 7
    C_USER_BIDIR_WPU,  # 8
    C_USER_BIDIR_WPU,  # 9
    C_USER_BIDIR_WPU,  # 10
    C_USER_BIDIR_WPU,  # 11
    C_USER_BIDIR_WPU,  # 12
    C_USER_BIDIR_WPU,  # 13
    C_USER_BIDIR_WPU,  # 14
    C_USER_BIDIR_WPU,  # 15
    C_USER_BIDIR_WPU,  # 16
    C_USER_BIDIR_WPU,  # 17
    C_USER_BIDIR_WPU,  # 18
]

del config_l[NUM_IO:]
