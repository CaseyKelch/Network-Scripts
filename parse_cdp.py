import re

with open("show_cdp_detail.txt", "r") as cdp_data:

    view_cdp = cdp_data.readlines()

    for line in view_cdp:

        if "Device ID: " in line:
            device = line.strip()
            device = re.sub(r"\.(.*)", "", device)
            print("-"*40)
            print("Remote " + device)

        if "Platform:" in line:
            plat = line.strip()
            plat = re.sub(r"\,(.*)", "", plat)
            plat = re.sub(r"Device ID: ", "", plat)
            print(plat)

        if "Interface:" in line:
            inter = line.strip()
            inter = re.sub(r"\,(.*)", "", inter)
            print("Local " + inter)

        if "Interface:" in line:
            pattern = re.compile(r'\): (.*)')
            outgo = line.strip()
            outgo = re.search(pattern, outgo)
            print("Remote Interface: " + ''.join(outgo.groups()))
