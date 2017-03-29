#!/usr/bin/python3

from time import sleep
from os import system
from cli import cli


def conn_check(host):
    # Connectivity Checker - 5 failed pings will exit loop.
    counter = 5
    succ_test = 1
    fail_test = 1
    ping = "ping -c 1 "  # Linux/nx-os
    while counter != 0:
        response = system(ping + host)
        if response == 0:
            counter = 5
            fail_test = 1
            print(host, " is up!", str(succ_test))
            succ_test += 1
            sleep(3)
        else:
            print(host, " is down!", str(fail_test))
            succ_test = 1
            counter -= 1
            fail_test += 1
            sleep(3)


def enable_interface(int):
    # Enables interface on Cisco Nexus device.
    cli("conf t ; interface " + int  + " ; no shut")
    print(int + " has been enabled.")
