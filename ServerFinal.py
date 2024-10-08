import hashlib
import socket 
import threading
import os
import tqdm
from ServerDetails import ServerDetails

#declaring constants to be used throughout the server

#List holding the files stored by the server
filesStored = []

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
disconnectMsg = "DISCONNECT"
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

#declaring the server socket variable
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#AF_INET specifies the type of addresses we are working with
#SOCK_STREAM specifies how data is transferred through socket

#associate server socket with the network interface and the port number being used
server.bind(ADDRESS)

#method that populates the filesStored list with the files stored by the server
def loadServerFiles():
    
    filesinServer = os.listdir('ServerFiles')
    for i in range(len(filesinServer)):
        file = filesinServer[i]
        line = file.split("&")
        name = "ServerFiles\\"+file
        ps = line[0]
        deet = ServerDetails(name, ps)
       
        filesStored.append(deet)

#method used to list all existing files in the server
def writeList():
    names = ""
    for i in range(len(filesStored)):
        useName = (filesStored[i].getFileName())
        names = names + useName + "\n"
    return names

#method handling threads of connecting clients
def handle_client (connection, address): 

    actionU = connection.recv(BUFFER_SIZE).decode(FORMAT)
    print(f"ACTION: {actionU}")

    if(actionU=="list"):
        strList=""
        l = []
        listOfNames = os.listdir('ServerFiles')
        for i in listOfNames:
            l.append(i.replace(i[:i.find("&")+1],""))
            strList=strList+(i.replace(i[:i.find("&")+1],""))+"\n"
        if(len(filesStored)==0):
            strList = "No files yet"

        connection.send(strList.encode())
        #connection.send(str(l).encode())

    else:
        received = connection.recv(BUFFER_SIZE).decode()

        key = "None"
        decK = "None"
        userKey = "None"
        
        if(actionU =="upload"):
            filename, filesize, hashValue = received.split(SEPARATOR)
            encryption = connection.recv(BUFFER_SIZE).decode()
            encryption = str(encryption)

            if(encryption=="yes"):
                userKey = connection.recv(BUFFER_SIZE).decode()
                userKey = str(userKey)

            dup = False
            stop=False

            namesUsed = writeList()
            namez = namesUsed.split("\n")
            for i in range(len(namez)):
                if(str(filename)==str(namez[i])):
                    print(f"There is a duplicate of this file named: "+str(filename))
                    dup=True
                    break

            if(dup):
                connection.send("duplicate".encode())
                action = connection.recv(BUFFER_SIZE).decode()
                if (action== "rename"):
                    stop = True
            else:
                connection.send("fine".encode())
                
            if(stop==False):
                #making sure the data is completely uploaded
                data = b''
                hashalue = ''
                while True:
                    chunk = connection.recv(1024)
                    if not chunk:
                        break
                    if not hashalue:
                        data += chunk
                       
                    if chunk.find(b''):
                        hashalue += chunk.decode()

                recHash = hashlib.sha256(data).hexdigest()

                with open("ServerFiles\\" +userKey+"&"+filename, 'wb') as f:
                        f.write(data)
                if recHash == hashValue:
                    print("File had been successfully transferred without corrupting!")

                else:
                    print(hashValue)
                    print(recHash)
                    print("File has been corrupted :(")

                #removing the duplicate item for overwrite
                if(dup):
                    strNm = str(filename)
                    for l in range(len(filesStored)):
                        if(strNm==str(filesStored[l].getFileName())):
                            os.remove(filesStored[l].getFileNameFull())
                            filesStored.remove(filesStored[l])
                            break
                    print("Duplicate has been removed.")

                details=ServerDetails(str("ServerFiles\\"+userKey +"&"+ filename), userKey)
                print("ServerDetails object created.")
                filesStored.append(details)

        elif(actionU=="download"):
            filename= received
            key = ""
            try: 
                for i in range(len(filesStored)):
                    if(filename==filesStored[i].getFileName()):
                        key = filesStored[i].getPassword()
                        break

                with (open("ServerFiles\\"+key+"&"+filename,'rb')) as f:
                    data = f.read()
                
                fileNum = None
                found = False
                passwd = "None"
            
                for i in range(len(filesStored)):
                    if(filename==filesStored[i].getFileName()):
                        fileNum=i
                        found = True
                        break
                        
                if(found):
                    if(filesStored[fileNum].getPassword() != "None"):
                                connection.send("protected".encode())
                                passwd = connection.recv(BUFFER_SIZE).decode()
                                if(passwd!=filesStored[fileNum].getPassword()):
                                    connection.send("That is the incorrect key".encode())
                                    
                                else:
                                    connection.send("cont".encode())
                                    
                    else:
                        connection.send("cont".encode())

                    chunkSize = 1024
                    totalSent = 0
                    while totalSent < len(data):
                        sent = connection.send(data[totalSent:totalSent+chunkSize])
                        if sent == 0:
                            break
                        totalSent += sent

            except FileNotFoundError as e:
                print(f"File {filename} not found!")
                connection.send(f"File {filename} not found!".encode())
                return
                
            
            connection.close()

#handles new connections and distributes them  
def start(): 
    server.listen()
    print(f"Serving at port {PORT} ")
    print(f"The Server IP is {SERVER}")
    while True:
        connection, address = server.accept() #connection = socket object
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f"Active connections: {threading.active_count()-1}")
    
print("Server Starting...")
loadServerFiles()

start()