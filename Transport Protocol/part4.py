import os
import subprocess # For incompatible os commands
import time
import signal

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