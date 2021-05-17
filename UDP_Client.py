import socket
import time
import os
import sys


def checkArg():
    if len(sys.argv) != 3:
        print("[ERROR] Enter Host Address and PORT number")
        sys.exit()
    else:
        print("Success!")


def checkPort():
    if int(sys.argv[2]) <= 5000:
        print("Enter PORT Number greater than 5000")
        sys.exit()
    else:
        print("Port number accepted!")


checkArg()
try:
    socket.gethostbyname(sys.argv[1])
except socket.error:
    print("Invalid host name. Exiting")
    sys.exit()

host = sys.argv[1]
try:
    port = int(sys.argv[2])
except ValueError:
    print("[ERROR] Incorrect port number.")
    sys.exit()
except IndexError:
    print("[ERROR] Incorrect port number.")
    sys.exit()

checkPort()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Client socket initialized")
    s.setblocking(0)
    s.settimeout(15)
except socket.error:
    print("Failed to create socket")
    sys.exit()

while True:
    command = input(
        "Choose one of the following options \n1. get <file>\n2. put <file>\n3. list\n4. exit\n ")
    CommClient = command.encode('utf-8')
    try:
        s.sendto(CommClient, (host, port))
    except ConnectionResetError:
        print("[ERROR] PORT numbers do not match!")
        sys.exit()
    CL = command.split()
    print("Proceeding... check Server for messages")

    if CL[0] == "get":
        print("Checking for acknowledgement")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print("[ERROR] PORT numbers do not match!")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)
        print("Inside Client Get")
        try:
            ClientData2, clientAddr2 = s.recvfrom(51200)
        except ConnectionResetError:
            print("[ERROR] PORT numbers do not match!")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()
        text2 = ClientData2.decode('utf8')
        print(text2)
        if len(text2) < 30:
            if CL[0] == "get":
                BigC = open("Received-" + CL[1], "wb")
                d = 0
                try:
                    CountC, countaddress = s.recvfrom(4096)
                except ConnectionResetError:
                    print("[ERROR] PORT numbers do not match!")
                    sys.exit()
                except:
                    print("Timeout or some other error")
                    sys.exit()
                tillC = CountC.decode('utf8')
                tillCC = int(tillC)
                print("Receiving packets will start now if file exists.")
                while tillCC != 0:
                    ClientBData, clientbAddr = s.recvfrom(4096)
                    dataS = BigC.write(ClientBData)
                    d += 1
                    print("Received packet number:" + str(d))
                    tillCC = tillCC - 1
                BigC.close()
                print("New Received file closed. Check contents in your directory.")

    elif CL[0] == "put":
        print("Checking for acknowledgement")
        try:
            ClientData, clientAddr = s.recvfrom(4096)
        except ConnectionResetError:
            print("[ERROR] PORT numbers do not match!")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)
        print("Sending data...")
        if text == "Valid Put command!":
            if os.path.isfile(CL[1]):
                c = 0
                size = os.stat(CL[1])
                sizeS = size.st_size  # number of packets
                print("File size in bytes: " + str(sizeS))
                Num = int(sizeS / 4096)
                Num = Num + 1
                print("Number of packets to be sent: " + str(Num))
                till = str(Num)
                tillC = till.encode('utf8')
                s.sendto(tillC, clientAddr)
                tillIC = int(Num)
                GetRun = open(CL[1], "rb")
                while tillIC != 0:
                    Run = GetRun.read(4096)
                    s.sendto(Run, clientAddr)
                    c += 1
                    tillIC -= 1
                    print("Packet number:" + str(c))
                    print("Data sending in process:")
                GetRun.close()
                print("Sent from Client - Put function")
            else:
                print("File does not exist.")
        else:
            print("Invalid.")

    elif CL[0] == "list":
        print("Checking for acknowledgement")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "[ERROR] PORT numbers do not match!")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)
        if text == "Valid List command!":
            ClientDataL, clientAddrL = s.recvfrom(4096)
            text2 = ClientDataL.decode('utf8')
            print(text2)
        else:
            print("Error. Invalid.")

    elif CL[0] == "exit":
        print("Server will exit if you have entered port number correctly")

    else:
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "[ERROR] PORT numbers do not match!")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)

print("END")
quit()
