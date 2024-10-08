
import hashlib
import socket 
import os
import sys
from colorama import Fore, Back, Style
from tkinter import *
#import tqdm

#defining constants and extracting command-line info
HEADER = 64
FORMAT = "utf-8"
SERVER = sys.argv[1]
PORT = sys.argv[2]
ADDRESS = (SERVER, int(PORT))
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #STREAM indictaes TCP socket

#function, when called upon, connects client to server
def connecter():
    client.connect(ADDRESS)

#displays a list of files currently available on the server to the client
def listFiles():
    files = client.recv(BUFFER_SIZE).decode("utf-8")
    print(files)
    quit()

#function reponsible for sending files from client-server
def sendFile():

    file = input("Enter filename :") #obtaining file name
    fileSize = os.path.getsize(file) #obtaining file size

    with (open(file,'rb')) as f:
        data = f.read() # reading data from file into data variable
    hashValue = hashlib.sha256(data).hexdigest() # obtains unique hashcode of data and sends to server

    client.send(f"{file}{SEPARATOR}{fileSize}{SEPARATOR}{hashValue}".encode()) 

    #portion of code responisble for encrypting files
    encryption = input("Encrypt file ('yes' / 'no')? ")
    client.send(encryption.encode())
    if(encryption=="yes"):
        custKey = input("What is the key? ") #obtains custom key from user
        client.send(custKey.encode()) #sends custom key to server

    #portion of code responsible for checking and resolving duplicate issues
    dupStatus = client.recv(BUFFER_SIZE).decode() #server tells client if the file being uploaded is a duplicate
    if (dupStatus=="duplicate"):
        act = input("There is already a file with that name, would you like to rename or overwrite the exsisting file ('rename' / 'overwrite')? ")
        client.send(act.encode())

    #portion of code responsible for sending file data from client to server
    chunkSize = 1024
    totalSent = 0
    while totalSent < len(data):
        sent = client.send(data[totalSent:totalSent+chunkSize])
        if sent == 0:
            break
        totalSent += sent
   
    client.close()

#function responsible for retieving files from server-client            
def FileRetriever():

    # obtaining the file name which the client wishes to recieve from the server & sending that name to the server
    FileName = input("Enter file name: ")
    client.send(f"{FileName}".encode(FORMAT))
    cont = "cont"
    enc = client.recv(BUFFER_SIZE).decode()
    
    #checks if requested file is protected or not
    if(enc=="protected"):
        giveKey = input("Enter the file key: ") #if protected, user is prompted for a key
        client.send(giveKey.encode())
        cont = client.recv(BUFFER_SIZE).decode()
        print("File has been successfully downloaded from the server!")
        #print(cont)

    #portion of code responsible for recieving file data in chunks from the server
    if(cont=="cont"):
        data = b''
        hashalue = ''
        while True:
            chunk = client.recv(1024)
            if not chunk:
                break
            if not hashalue:
                data += chunk
            if chunk.find(b''):
                hashalue += chunk.decode()
       
        with open("Client_Files\\"+FileName, 'wb') as writtenFile:
            writtenFile.write(data)
        writtenFile.close()
    else:
        print("wrong key")

print(Fore.RED +f"Welcome to the server {os.getlogin()}!")
print(Style.RESET_ALL)

if ( input("Enter 'connect' to connect to server or 'Q' to quit: ") == 'connect'):
   connecter()
else:
    print(f"Goodbye {os.getlogin()}!")
    quit()

commandLineArgs = sys.argv[3]
client.send(commandLineArgs.encode())

if(commandLineArgs == "upload"):
    sendFile()
elif(commandLineArgs == "download"):
    FileRetriever()
elif(commandLineArgs == "list"):
    listFiles()
  
else:
    print("Your command is not recognised by the server.")
    quit()
quit()
