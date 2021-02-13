import os

def uniqueEntries(input, names, uniqueList):
    """
    Function removes unnecessary columns and returns list of unique entries
    """
    rowNumber = 0
    for row in input:
        line = row.split()

        # Get source and destination IPs
        # Columns 4 is an arrow, we do not want that
        rowContent = ""
        for column in range(2,5):
            if column == 3:
                continue
            else:
                rowContent += line[column] + " "
        
        # Add server names
        # From serverNames.txt, each line has a newline character, it must be replaced (stripping also works with rstrip() and appending a space)
        rowContent += names[rowNumber]
        rowContent = rowContent.replace("\n", " ")

        # Get and add organizations
        # Split twice, once by field then by line to get only the organization name
        # Append newline since second split removed newlines
        elements = rowContent.split()
        os.system("whois " + elements[1] + " > org.txt")
        organizations = open("org.txt", 'r')
        orgContent = organizations.read().split("OrgName:        ")
        split = orgContent[1].split("\n")
        rowContent += split[0] + '\n'

        # Add unique elements only
        uniqueList.add(rowContent)
        rowNumber += 1  
    return uniqueList    

os.system("tshark -r adBlock.pcap -w temp.pcap ssl.handshake.type == 1")
os.system("tshark -r temp.pcap > input.txt")
os.system("tshark -r temp.pcap -T fields -e tls.handshake.extensions_server_name > serverNames.txt")

input = open("input.txt", "r")
serverNames = open("serverNames.txt", "r")
output = open("output.txt", "w")

names = serverNames.readlines()

uniqueList = set()
uniqueList = uniqueEntries(input, names, uniqueList)

output.writelines(uniqueList)

input.close()
serverNames.close()
output.close()