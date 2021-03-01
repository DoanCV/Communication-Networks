import os # Terminal execution
from socket import getservbyport # For service conversion

"""
organize output into a class:
    objects:
        port:
        "port -> port" + "/tcp"

        state:
            syn filtered, after arrow
            syn,ack open, before arrow

        services:
            21 = ftp
            22 = ssh
            23 = telnet
            25 = smtp
            80 = http
            110 = pop3
            139 = netbios-ssn
            443 = https
            445 = microsoft-ds
            3389 = ms-wbt-server
                anything else, which is now the default case, use getservbyport()
"""
class port:
    def __init__(self, prt, st):
        self.prt = prt
        self.st = st
        self.serv = getservbyport(int(prt))

def parse(openState, filteredState, text):
    for line in text:
        content = line.split()

        if content[10] == "[SYN,":
            openState.add(content[7])
        elif content[10] == "[SYN]":
            filteredState.add(content[9])
        else:
            continue
    return

os.system("tshark -r feb11_nmap.pcap > feb11_nmap.txt")
text = open("feb11_nmap.txt", "r")

openState = set()
filteredState = set()
parse(openState, filteredState, text)

ports = []

for i in filteredState:
    ports.append(port(i, 'filtered'))

for i in openState:
    for port in ports:
        if port.prt == i:
            port.st = "open"  
        else:
            continue

ports.sort(key = lambda x: int(x.prt))

for port in ports:
    print(port.prt + "/tcp " + port.st + " " + port.serv)

text.close()