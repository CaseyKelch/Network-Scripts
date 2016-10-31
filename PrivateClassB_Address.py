#!/usr/bin/python3
"""
Writes 172.16.0.0/12 address space to file.
"""


ip = "172."
octet_two = 16
octet_three = 0
octet_four = 0
count = 1

f = open("ip_list.txt", "w")

while octet_three != 256 and octet_four != 256 and octet_two != 32:
    f.write(ip + str(octet_two) + "." + str(octet_three) + "." + str(octet_four) + " ***!" + str(count) + "\n")
    octet_four += 1
    count += 1

    if octet_three == 255 and octet_four == 256:
        octet_two += 1
        octet_three = 0
        octet_four = 0

    elif octet_four == 256:
        octet_three += 1
        octet_four = 0

f.close()
