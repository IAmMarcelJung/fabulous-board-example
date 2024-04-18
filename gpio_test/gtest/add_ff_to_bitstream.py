import argparse


def add_ff_to_bitstream(bitstream_file):
    with open(bitstream_file, "r") as f:
        contents = f.readlines()

    insert = "    "
    for i in range(128):
        insert += "0xFF, "
        if (i % 12) == 0 and (i != 0):
            insert += "\n    "
    insert += "\n"
    contents.insert(4, insert)

    with open(bitstream_file, "w") as f:
        f.writelines(contents)


def add_size_of_bitstream():
    pass


def calc_num_of_bytes():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="add_ff_to_bitstream",
        description="Add 0xFF 128 times before the other bytes of the bitstream.",
    )
    parser.add_argument("bitstream")
    args = parser.parse_args()
    add_ff_to_bitstream(args.bitstream)
