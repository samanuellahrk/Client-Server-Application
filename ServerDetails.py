#Class used to store objects that contain information on the files stored in the server

class ServerDetails:
    #initializing the information
    def __init__(self, fileName,password):
        self.fileName = fileName
        self.password = password


#accessor methods
    def getFileName(self):
        nm = self.fileName
        ind = nm.find("&")+1
        newStr = nm[ind:]
        return newStr
    
    def getFileNameFull(self):
        return self.fileName
    
    def getPassword(self):
        return self.password

