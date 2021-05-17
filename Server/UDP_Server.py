import socket
import time
import os
import sys


def checkArg():
    if len(sys.argv) != 2:
        print("[ERROR] Enter Host Address and PORT number")
        sys.exit()
    else:
        print("Success!")


def checkPort():
    if int(sys.argv[1]) <= 5000:
        print("Enter PORT Number greater than 5000")
        sys.exit()
    else:
        print("Port number accepted!")


def ServerList():
    print("Sending Acknowledgment of command.")
    msg = "Valid List command!"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Message Sent to Client.")
    print("In Server, List function")
    F = os.listdir(
        path="C:/Kevin's Stuff/University Files/Sixth Semester/Computer Networks/Project/Server")
    Lists = []
    for file in F:
        Lists.append(file)
    ListsStr = str(Lists)
    ListsEn = ListsStr.encode('utf-8')
    s.sendto(ListsEn, clientAddr)
    print("List sent from Server")


def ServerExit():
    print("System will gracefully exit! Not sending any message to Client. Closing my socket!")
    s.close()
    sys.exit()


def ServerGet(g):
    print("Sending Acknowledgment of command.")
    msg = "Valid Get command!"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Message Sent to Client.")
    print("In Server, Get function")
    if os.path.isfile(g):
        msg = "File exists"
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        print("Message about file existence sent.")
        c = 0
        sizeS = os.stat(g)
        sizeSS = sizeS.st_size  # number of packets
        print("File size in bytes:" + str(sizeSS))
        NumS = int(sizeSS / 4096)
        NumS = NumS + 1
        tillSS = str(NumS)
        tillSSS = tillSS.encode('utf8')
        s.sendto(tillSSS, clientAddr)
        check = int(NumS)
        GetRunS = open(g, "rb")
        while check != 0:
            RunS = GetRunS.read(4096)
            s.sendto(RunS, clientAddr)
            c += 1
            check -= 1
            print("Packet number:" + str(c))
            print("Data sending in process:")
        GetRunS.close()
        print("Sent from Server - Get function")
    else:
        msg = "[ERROR] File does not exist in Server directory."
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        print("Message Sent.")


def ServerPut():
    print("Sending Acknowledgment of command.")
    msg = "Valid Put command!"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Message Sent to Client.")
    print("In Server, Put function")
    if t2[0] == "put":
        BigSAgain = open(t2[1], "wb")
        d = 0
        print("Receiving packets will start now if file exists.")
        try:
            Count, countaddress = s.recvfrom(4096)  # number of packet
        except ConnectionResetError:
            print("[ERROR] PORT numbers do not match!")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()
        tillI = Count.decode('utf8')
        tillI = int(tillI)
        while tillI != 0:
            ServerData, serverAddr = s.recvfrom(4096)
            dataS = BigSAgain.write(ServerData)
            d += 1
            tillI = tillI - 1
            print("Received packet number:" + str(d))
        BigSAgain.close()
        print("New file closed. Check contents in your directory.")


def ServerElse():
    msg = "[ERROR] " + t2[0] + " is not recognized by server"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Message Sent.")


host = ""
checkArg()
try:
    port = int(sys.argv[1])
except ValueError:
    print("[ERROR] Invalid PORT number")
    sys.exit()
except IndexError:
    print("[ERROR] Invalid PORT number")
    sys.exit()
checkPort()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Server socket initialized")
    s.bind((host, port))
    print("Successful binding. Waiting for Client now.")
except socket.error:
    print("Failed to create socket")
    sys.exit()

while True:
    try:
        data, clientAddr = s.recvfrom(4096)
    except ConnectionResetError:
        print(
            "[ERROR] PORT numbers do not match!")
        sys.exit()
    text = data.decode('utf8')
    t2 = text.split()
    if t2[0] == "get":
        print("RRQ received from: ", clientAddr)
        ServerGet(t2[1])
    elif t2[0] == "put":
        print("WRQ received from: ", clientAddr)
        ServerPut()
    elif t2[0] == "list":
        print("List received from: ", clientAddr)
        ServerList()
    elif t2[0] == "exit":
        print("Exiting...")
        ServerExit()
    else:
        ServerElse()

print("END")
quit()
