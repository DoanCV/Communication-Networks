import os
import subprocess # For incompatible os commands
import time
import signal
from socket import getservbyport # For service conversion

# website: github.com
# portsList: 21,22,23,25,80,443

target = input("Enter website:\n")
portsList = input("Enter ports, specified as a comma delimited list without spaces:\n")

process = subprocess.Popen(["sudo", "tcpdump", "tcp", "-w", "part4.pcap"])
pid = process.pid

# Time to type in password for the first time running this program
time.sleep(5)

portsList = portsList.split(",")
for content in portsList:
    print("Connecting to: " + target + "\n" + "Scanning port: " + content + "\n")
    # netcat command
    os.system("nc -w 3 " + target + " " + content)

# Wait for 2 seconds since the process
time.sleep(2)
process.terminate()
time.sleep(2)

"""
From #3
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

os.system("tshark -r part4.pcap > part5.txt")
text = open("part5.txt", "r")

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