from asyncore import write
from distutils.log import error
import json
import ipaddress 
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import datetime


def send_command(device, commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                print(command)
                output = ssh.send_command(command, expect_string=r"%|>")
                print(output)
                result[command] = output
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


def getConfig(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            output = ssh.send_command(command, expect_string=r"%|>")
            # w  >>> Opens a file for writing. Creates a new file if it does not exist or truncates the file if it exists.
            with open(str(fileNameString), 'w') as f:
                for line in output:
                    f.write(line)
        return True
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


def validate_ip_address(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        print("IP address {} is not valid".format(address)) 

if __name__ == "__main__":
    current_time = datetime.datetime.today().strftime('%Y_%b_%d')
    hosts = json.load(open("hosts.json"))
    fileNameString = 'Backup_' + \
        str(hosts['host']) + '_' + str(current_time) + '_displayset.txt'
    select_Mode = input(
        "Which one? Use Command_Set.txt (1) or Wizard Mode (2) : ")
    if select_Mode == "1":
        # Commands from File
        with open('Command_Set.txt') as f:
            CM_Set = [line.rstrip('\n') for line in f]
            #print(CM_Set)
            send_command(hosts, CM_Set)
            getConfig(hosts, "show configuration | display set")
    elif select_Mode == "2":
        # Commands for backup and received Tftp server address from input
        TFTP_SRV = input(str("Please enter tftp server ip: "))
        if validate_ip_address(TFTP_SRV) == True:
            CM_Set = ["cli", "start shell", "cd /config", "tftp",
                    "connect "+TFTP_SRV, "put rescue.conf.gz"]
            send_command(hosts, CM_Set)
            getConfig(hosts, "show configuration | display set")
            
    else:
        print ("wrong input!")



