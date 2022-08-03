from asyncio import tasks
import requests
import os
import datetime
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result
from nornir.core.exceptions import NornirExecutionError
import logging

def save_config_to_file(type, hostname, config):
    filename = f"{hostname}_{dateTime}.cfg"
    if type == "ssh":
        with open(os.path.join(BACKUP_DIR, filename), "w",encoding="utf-8") as f:
            f.write(config)
        print(f"{hostname} >>> backup file was created successfully!")
    elif type == "http":
        with open(os.path.join(BACKUP_DIR, filename), "wb") as f:
                f.write(config.content)
        print(f"{hostname} >>> backup file was created successfully!")
    else:
        print("Hostname is unknown!")

def get_juniper_backups()-> Result:
    junos = nr.filter(platform="junos")
    backup_results = junos.run(
        task=netmiko_send_command,
        command_string="show config | display set",severity_level=logging.DEBUG)
    print_result(backup_results)
    for hostname in backup_results:
        save_config_to_file(
            type="ssh",
            hostname=hostname,
            config=backup_results[hostname][0].result,)

def get_fortinet_backups()-> Result:
    fortinet_http = nr.filter(platform="fortinet", type="http")
    print("***************** Fortinet_HTTP *****************")
    for host in fortinet_http.inventory.hosts:
        hostname = fortinet_http.inventory.hosts[host].hostname
        port = fortinet_http.inventory.hosts[host].port
        access_token = fortinet_http.inventory.hosts[host].password
        requests.packages.urllib3.disable_warnings()
        apiUrl = f"https://{hostname}:{port}/api/v2/monitor/system/config/backup?scope=global&access_token={access_token}"
        # print(apiUrl)
        payload = {}
        data = requests.request("GET",apiUrl, verify=False,data=payload)
        save_config_to_file(type="http", hostname=host, config=data)

def get_fortinet_ssh_backup() -> Result:
        fortinet_ssh = nr.filter(platform="fortinet", type="ssh")
        #try:
        backup_results = fortinet_ssh.run(
        task=netmiko_send_command,
        command_string="show",severity_level=logging.DEBUG)
        print_result(backup_results)
        for host in backup_results:
            save_config_to_file(
                type="ssh",
                hostname=host,
                config=backup_results[host][0].result,)
            
if __name__ == "__main__":
    nr = InitNornir('config.yaml',core={"raise_on_error": True})
    BACKUP_DIR = "."
    dateTime = datetime.datetime.today().strftime('%Y_%m_%d_%H_%M')
    FTP = "192.168.100.13"
    get_juniper_backups()
    get_fortinet_backups()
    get_fortinet_ssh_backup()
