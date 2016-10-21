'''
Python 3.4 Script will take csv file of mac address list
and locate interfaces - Tkinter GUI.
'''

import paramiko
import time
import os
import sys
import csv
import re
import getpass
from tkinter import *
#Enable GUI
root = Tk()
#GUI
def assignVariables():
    global ip
    ip = IP_Entry.get()
    global username
    username = User_Entry.get()
    global password
    password = Pass_Entry.get()
    global InterfaceType
    InterfaceType = Interface_Entry.get()
    global MACAddressList
    MACAddressList = MAC_Entry.get()
    global VoiceVLAN
    VoiceVLAN = VLAN_Entry.get()
    root.withdraw()
    root.quit()

#Disable Paging Function
def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

#This function defines unique output.  Is used to not get duplicate interface output.
def uniq(input):
  output = []
  for x in input:
    if x not in output:
      output.append(x)
  return output


#Start of program
if __name__ == '__main__':
    # main program

    # VARIABLES TO BE CHANGED
    root.title("Alta Voice VLAN Editor")
    root.geometry("400x300")

    IP_Field = Label(root, text="IP or Hostname")
    IP_Field.pack()
    IP_Entry = StringVar()
    Entry(root, textvariable=IP_Entry, width=40).pack()

    User_Field = Label(root, text="Username")
    User_Field.pack()
    User_Entry = StringVar()
    Entry(root, textvariable=User_Entry, width=40).pack()

    Pass_Field = Label(root, text="Password")
    Pass_Field.pack()
    Pass_Entry = StringVar()
    Entry(root, textvariable=Pass_Entry, show="*", width=40).pack()

    Interface_Field = Label(root, text="Interface\n(Gi, GigabitEthernet, FastEthernet)")
    Interface_Field.pack()
    Interface_Entry = StringVar()
    Entry(root, textvariable=Interface_Entry, width=40).pack()

    MAC_Field = Label(root, text="MAC List Directory")
    MAC_Field.pack()
    MAC_Entry = StringVar()
    Entry(root, textvariable=MAC_Entry, width=40).pack()


    VLAN_Field = Label(root, text="Voice VLAN")
    VLAN_Field.pack()
    VLAN_Entry = StringVar()
    Entry(root, textvariable=VLAN_Entry, width=40).pack()

    Button(root, text='Submit', command=assignVariables).pack()
    root.mainloop()

    #command = input('Enter command:')

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
         paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    print("\nSSH connection established to %s" % ip + '...')

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    #print("Interactive SSH session established")

    # Strip the initial router prompt
    output = remote_conn.recv(1000)

    # See what we have
    #print(output)

    # Turn off paging
    disable_paging(remote_conn)

    # Send router command variable defined by user input
    remote_conn.send("\n")
    #remote_conn.send(command + "\n")

    #This looks at MAC File and sends each line to SSH shell
    showMAC = 'show mac add add '
    with open(MACAddressList, 'r') as csvfile:
        macReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for mac in macReader:
            remote_conn.send(showMAC + ', '.join(mac) + '\n')
            #time.sleep(1)

    # Wait for the command to complete
    time.sleep(10)

    #Modify bytes of output
    output = remote_conn.recv(500000)
    
    show_command = output
    #Save output of show_command to csv file
    createCSV = open('C:\\Users\\'+ username+'\\'+ip+'MacTable.csv', 'w')
    fd = os.open('C:\\Users\\'+ username+'\\'+ip+'MacTable.csv',os.O_RDWR)
    ret = os.write(fd,show_command)
    os.close(fd)

    print('\nMacTable successfully written to C:\\Users\\'+ username+'\\'+ip+'MacTable.csv\n')
    #############################################################################

    ##RegEx for  'Gi1/0/1' etc...
    intPattern = re.compile(r''+ InterfaceType + '\d\/\d\/\d*|\d\/\d*')

    #findInterfaces = intPattern.findall(show_command)
    show_command = str(show_command)
    foundInterfaces = (re.findall(intPattern, show_command))
    uniqfoundInterfaces = uniq(foundInterfaces) 
    print('...Voice VLAN ' + VoiceVLAN + ' Configuration For ' + ip + ' below...\n')
    print('!' + ip)

    interfaceNumber = 0

    outputinterfaceNumber = 0
    #Output configuration to screen
    if InterfaceType == 'FastEthernet':
        #Write Configuration to file.
        for interfaces in uniqfoundInterfaces:
            with open('C:\\Users\\'+ username+'\\'+ip+'VLANConfig.csv', 'a') as f:
                print('interface ' + InterfaceType + interfaces + '\n switchport voice vlan ' + VoiceVLAN, file = f)
                interfaceNumber = interfaceNumber + 1
                print('!'+ str(interfaceNumber), file = f)

        for interfaces in uniqfoundInterfaces:
            print('interface ' + InterfaceType + interfaces + '\n switchport voice vlan ' + VoiceVLAN)
            outputinterfaceNumber = outputinterfaceNumber + 1
            print('!'+ str(outputinterfaceNumber))

    else:
        #Write Configuration to file.
        for interfaces in uniqfoundInterfaces:
            with open('C:\\Users\\'+ username+'\\'+ip+'VLANConfig.csv', 'a') as f:
                print('interface ' + interfaces + '\n switchport voice vlan ' + VoiceVLAN, file = f)
                interfaceNumber = interfaceNumber + 1
                print('!'+ str(interfaceNumber), file = f)

        for interfaces in uniqfoundInterfaces:
            print('interface ' + interfaces + '\n switchport voice vlan ' + VoiceVLAN)
            outputinterfaceNumber = outputinterfaceNumber + 1
            print('!'+ str(outputinterfaceNumber))
    root = Tk()
    root.title("Alta Voice VLAN Editor")
    root.geometry("270x120")
    directoryFile = '\n\nConfiguration has been written to:\nC:\\Users\\'+ username+'\\'+ip+'VLANConfig.csv\n\n'
    EndApp = Label(root, text=directoryFile)
    EndApp.pack()
    Button(root, text='Exit', command=assignVariables).pack()
    root.mainloop()      
    #print('\nConfiguration has been written to C:\\Users\\'+ username+'\\'+ip+'VLANConfig.csv')
    #input('\nPress Enter to Exit...')

