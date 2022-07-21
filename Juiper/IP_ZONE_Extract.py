import json

backupFileName = input("Enter Backup File Name: ")
grpName = input("Group Name: ")
listofIPs = json.load(open("listofIPs.json"))
with open(backupFileName) as f:
    backupFile = f.readlines()
    addressBook = open("address_book.txt", "a")
    for line in backupFile:
        if "security address-book" in line:
            addressBook.write(line)
    addressBook.close()
    f.close()
# Extract Zone and IP then write with command set to the file
with open("address_book.txt") as AB:
    addressBook = AB.readlines()
    commandSet = open("command_set_ip.txt", "w")
    for line in addressBook:
        lineSplitted = line.split(" ")
        AB = list(filter(lambda ip: ip in line, listofIPs))
        if AB:
            commandSet.write(
                f"set logical-systems Behsazan security address-book {lineSplitted[5]} address-set {grpName} address {lineSplitted[7]}\n")
