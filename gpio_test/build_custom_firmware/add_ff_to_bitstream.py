with open("bitstream.h", "r") as f:
    contents = f.readlines()

insert = "    "
for i in range(128):
    insert += "0xFF, "
    if (i % 12) == 0 and (i != 0):
        insert += "\n    "
insert += "\n"
contents.insert(4, insert)

with open("bitstream.h", "w") as f:
    f.writelines(contents)
