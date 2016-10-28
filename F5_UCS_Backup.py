#!/usr/bin/python3

import paramiko
import time
import datetime
import base64
from collections import OrderedDict


class F5Backup:

    def __init__(self, sorteddict, username, password, directory):
        self.sorteddict = sorteddict
        self.username = username
        self.password = password
        self.directory = directory

    """
    UCS Backup Creation
    """

    def archive_ucs(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        for ip, f5host in self.sorteddict.items():
            ssh.connect(ip, username=self.username, password=self.password)
            ssh.exec_command("tmsh save /sys ucs /var/tmp/"+f5host+"{:%m-%d-%Y}".format(datetime.datetime.now())+".ucs")
            time.sleep(30)
            ssh.close()

    """
    SFTP UCS file from F5 to Directory
    """

    def sftp_ucs(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        for ip, f5host in self.sorteddict.items():
            ssh.connect(ip, username=self.username, password=self.password)
            sftp = ssh.open_sftp()
            sftp.get("/var/tmp/"+f5host+"{:%m-%d-%Y}".format(datetime.datetime.now())+".ucs", self.directory +
                     f5host+"{:%m-%d-%Y}".format(datetime.datetime.now())+".ucs")
            sftp.close()
            ssh.close()

    """
    Cleanup UCS files from F5 /var/tmp directory.
    """

    def cleanup_ucs(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        for ip, f5host in self.sorteddict.items():
            ssh.connect(ip, username=self.username, password=self.password)
            ssh.exec_command("rm /var/tmp/*.ucs")
            time.sleep(2)
            ssh.close()


"""
-Sample-
"""
f5_dict = {
            "1.1.1.1": "F5_Host_1", "1.1.1.2": "F5_Host_2"
           }
f5_sorted = OrderedDict(sorted(f5_dict.items()))
user = 'admin'
passw = base64.b64decode('xxxxx').decode('ascii')
my_dir = "C:\\Desktop\\F5"

backup = F5Backup(f5_sorted, user, passw, my_dir)
backup.archive_ucs()
backup.sftp_ucs()
backup.cleanup.ucs()
