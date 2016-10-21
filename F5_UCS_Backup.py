#!/usr/bin/python3


# Python Libraries
import paramiko
import time
import datetime
import smtplib
import base64
from collections import OrderedDict


# Credentials
username = 'admin'
password = base64.b64decode('xxxxx').decode('ascii')

# Dictionary with IP as key with Hostname value
f5_dict = {
            "1.1.1.1": "F5_Host_1", "1.1.1.2": "F5_Host_2"
           }


# Sorts dictionary so that results are consistent.  Orders by IP address(Key).
f5_sorted = OrderedDict(sorted(f5_dict.items()))


"""
Generate UCS backup
"""


def backup_ucs(sorteddict):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for ip, f5host in sorteddict.items():
        ssh.connect(ip, username=username, password=password)
        ssh.exec_command("tmsh save /sys ucs /var/tmp/"+f5host+"{:%m-%d-%Y}".format(datetime.datetime.now())+".ucs")
        time.sleep(30)
        ssh.close()

"""
SFTP UCS file from F5 to NEESRV5012
"""


def sftp_ucs(sorteddict):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for ip, f5host in sorteddict.items():
        ssh.connect(ip, username=username, password=password)
        sftp = ssh.open_sftp()
        sftp.get("/var/tmp/"+f5host+"{:%m-%d-%Y}".format(datetime.datetime.now())+".ucs", "C:\\"+
                 f5host+"{:%m-%d-%Y}".format(datetime.datetime.now())+".ucs")
        sftp.close()
        ssh.close()

"""
Cleanup UCS files from F5 /var/tmp directory.
"""


def cleanup_ucs(sorteddict):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for ip, f5host in sorteddict.items():
        ssh.connect(ip, username=username, password=password)
        ssh.exec_command("rm /var/tmp/*.ucs")
        time.sleep(2)
        ssh.close()



