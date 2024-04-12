# gpio_config_def.py file for part 6
# io_config -- version 1.2.2
voltage = 1.80
analog = False

H_NONE = 0
H_DEPENDENT = 1
H_INDEPENDENT = 2
H_SPECIAL = 3
H_UNKNOWN = 4

# voltage: 1.8
# IO configuration chain was successful
gpio_l = [
    ["IO[0]", H_NONE],
    ["IO[1]", H_INDEPENDENT],
    ["IO[2]", H_DEPENDENT],
    ["IO[3]", H_DEPENDENT],
    ["IO[4]", H_DEPENDENT],
    ["IO[5]", H_DEPENDENT],
    ["IO[6]", H_DEPENDENT],
    ["IO[7]", H_INDEPENDENT],
    ["IO[8]", H_DEPENDENT],
    ["IO[9]", H_DEPENDENT],
    ["IO[10]", H_INDEPENDENT],
    ["IO[11]", H_INDEPENDENT],
    ["IO[12]", H_INDEPENDENT],
    ["IO[13]", H_INDEPENDENT],
    ["IO[14]", H_INDEPENDENT],
    ["IO[15]", H_INDEPENDENT],
    ["IO[16]", H_INDEPENDENT],
    ["IO[17]", H_INDEPENDENT],
    ["IO[18]", H_INDEPENDENT],
]
# voltage: 1.8
# configuration failed in gpio[28], anything before is invalid
gpio_h = [
    ["IO[37]", H_NONE],
    ["IO[36]", H_INDEPENDENT],
    ["IO[35]", H_INDEPENDENT],
    ["IO[34]", H_INDEPENDENT],
    ["IO[33]", H_INDEPENDENT],
    ["IO[32]", H_INDEPENDENT],
    ["IO[31]", H_INDEPENDENT],
    ["IO[30]", H_INDEPENDENT],
    ["IO[29]", H_INDEPENDENT],
    ["IO[28]", H_UNKNOWN],
    ["IO[27]", H_UNKNOWN],
    ["IO[26]", H_UNKNOWN],
    ["IO[25]", H_UNKNOWN],
    ["IO[24]", H_UNKNOWN],
    ["IO[23]", H_UNKNOWN],
    ["IO[22]", H_UNKNOWN],
    ["IO[21]", H_UNKNOWN],
    ["IO[20]", H_UNKNOWN],
    ["IO[19]", H_UNKNOWN],
]
