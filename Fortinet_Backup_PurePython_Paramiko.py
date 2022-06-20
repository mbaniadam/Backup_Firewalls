import paramiko


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("x.x.x.x",username='admin',password='----') 
stdin, stdout, stderr=ssh.exec_command("execute backup config tftp FortiBackup y.y.y.y")
stdout.readlines()
ssh.close()
