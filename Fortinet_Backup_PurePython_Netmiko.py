from asyncore import write
from netmiko import ConnectHandler
import datetime
BFG = {'host':'Forti',
        'device_type':'fortinet', 'ip':'x.x.x.x',
        'username': 'admin' , 'password':'---' }

fg_connect = ConnectHandler(**BFG)
output = fg_connect.send_command('show full-configuration')
current_time = datetime.datetime.today().strftime('%Y_%b_%d')

#w  >>> Opens a file for writing. Creates a new file if it does not exist or truncates the file if it exists.
with open('Backup_' + str(BFG['host']) + '_' + str(current_time) + '.cfg', 'w') as f:
    for line in output:
        f.write(line)

