import requests
import os
import datetime
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from napalm.base import get_network_driver
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

def save_config_to_file(type, hostname, config):
    filename = f"{hostname}-{dateTime}.cfg"
    if type == "ssh":
        with open(os.path.join(BACKUP_DIR, filename), "w") as f:
            f.write(config)
        return True
    elif type == "http":
        with open(os.path.join(BACKUP_DIR, filename), "wb") as f:
            for line in config:
                f.write(line)
        print(f"{hostname} Backup is succesful!")
        return True
    else:
        print("Hostname is unknown!")
        return False

def get_juniper_backups():
    junos = nr.filter(platform="junos")
    backup_results = junos.run(
        task=netmiko_send_command,
        command_string="show config | display set")

    for hostname in backup_results:
        if save_config_to_file(
                type="ssh",
                hostname=hostname,
                config=backup_results[hostname][0].result,):
            print(f"{hostname} Backup is succesful!")
            # print("changed: ", backup_results[hostname].changed)
            # print("failed: ", backup_results[hostname].failed)


def get_fortinet_backups():
    fortinet_http = nr.filter(platform="fortinet", type="http")
    fortinet_ssh = nr.filter(platform="fortinet", type="ssh")
    hostname = fortinet_http.inventory.hosts[host].hostname
    port = fortinet_http.inventory.hosts[host].port
    access_token = fortinet_http.inventory.hosts[host].password
    for host in fortinet_http.inventory.hosts:
        requests.packages.urllib3.disable_warnings()
        apiUrl = f"https://{hostname}:{port}/api/v2/monitor/system/config/backup?scope=global&access_token={access_token}"
        # print(apiUrl)
        data = requests.get(apiUrl, verify=False)
        save_config_to_file(type="http", hostname=host, config=data)
    backup_results = fortinet_ssh.run(
        task=netmiko_send_command,
        command_string="show")
    for hostname in backup_results:
        if save_config_to_file(
                type="ssh",
                hostname=hostname,
                config=backup_results[hostname][0].result,):
            print(f"{hostname} Backup is succesful!")

if __name__ == "__main__":
    nr = InitNornir('config.yaml')
    BACKUP_DIR = "."
    dateTime = datetime.datetime.today().strftime('%Y_%b_%d')
    FTP = "192.168.1.100"
    get_juniper_backups()
    get_fortinet_backups()
