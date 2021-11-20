'''
Script for client side
@author: hao
'''
import protocol
import config
from socket import *
import os
import time

class client:
    
    fileList=[] # list to store the file information
    uploadFileList=[] #JT List to store the local files to upload

    #Constructor: load client configuration from config file
    #JT Added upload path to client configuration.
    def __init__(self):
        self.serverName, self.serverPort, self.clientPort, self.downloadPath, self.uploadPath = config.config().readClientConfig()

    # Function to produce user menu 
    #JT Added updates to menu for uploading files to server
    def printMenu(self):
        print("Welcome to simple file sharing system!")
        print("Please select operations from menu")
        print("--------------------------------------")
        print("1. Review the List of Available Files to Download")
        print("2. Review the List of Available Files to Upload")
        print("3. Download File")
        print("4. Upload File")
        print("5. Quit")

    # Function to get user selection from the menu
    # JT Updated function for the additional options.
    def getUserSelection(self):       
        ans=0
        # only accept option 1-5
        while ans>5 or ans<1:
            self.printMenu()
            try:
                ans=int(input())
            except:
                ans=0
            if (ans<=5) and (ans>=1):
                return ans
            print("Invalid Option")

    # Build connection to server
    def connect(self):
        serverName = self.serverName
        serverPort = self.serverPort
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName,serverPort))
        return clientSocket

    # JT. New function to get local files to upload
    def getLocalFileList(self):
        self.uploadFileList = os.listdir(self.uploadPath)

    # JT. New function to get print local files to upload
    def printLocalFileList(self):
        count=0
        for f in self.uploadFileList:
            count+=1
            print('{:<3d}{}'.format(count,f))
        

    # Get file list from server by sending the request
    def getFileList(self):
        mySocket=self.connect()
        mySocket.send(protocol.prepareMsg(protocol.HEAD_REQUEST," "))
        header, msg=protocol.decodeMsg(mySocket.recv(1024).decode())
        mySocket.close()
        if(header==protocol.HEAD_LIST): 
            files=msg.split(",")
            self.fileList=[]
            for f in files:
                self.fileList.append(f)
        else:
            print ("Error: cannnot get file list!")

    # function to print files in the list with the file number
    def printFileList(self):
        count=0
        for f in self.fileList:
            count+=1
            print('{:<3d}{}'.format(count,f))

    # Function to select the file from file list by file number,
    # return the file name user selected
    def selectDownloadFile(self):
        if(len(self.fileList)==0):
            self.getFileList()
        ans=-1
        while ans<0 or ans>len(self.fileList)+1:
            self.printFileList()
            print("Please select the file you want to download from the list (enter the number of files):")
            try:
                ans=int(input())
            except:
                ans=-1
            if (ans>0) and (ans<len(self.fileList)+1):
                return self.fileList[ans-1]
            print("Invalid number")

    
    #JT Added new function to select file to upload.
    def selectUploadFile(self):
        if(len(self.uploadFileList)==0):
            self.getLocalFileList()
        ans=-1
        while ans<0 or ans>len(self.uploadFileList)+1:
            self.printLocalFileList()
            print("Please select the file you want to upload from the list (enter the number of files):")
            try:
                ans=int(input())
            except:
                ans=-1
            if (ans>0) and (ans<len(self.uploadFileList)+1):
                return self.uploadFileList[ans-1]
            print("Invalid number")

    # Function to send download request to server and wait for file data
    def downloadFile(self,fileName):
        mySocket=self.connect()
        mySocket.send(protocol.prepareMsg(protocol.HEAD_DOWNLOAD, fileName))
        with open(self.downloadPath+"/"+fileName, 'wb') as f:
            #print ('file opened')
            while True:
                #print('receiving data...')
                data = mySocket.recv(1024)
                #print('data=%s', (data))
                if not data:
                     break
            # write data to a file
                f.write(data)
        print(fileName+" has been downloaded!")
        mySocket.close()


    # Function to send upload request to server 
    #JT Created function to upload the selected file.
    def uploadFile(self,fileName):
        mySocket=self.connect()
        mySocket.send(protocol.prepareMsg(protocol.HEAD_UPLOAD, fileName))
        #JT Without the sleep here the message that was sent to the server was the
        #JT filename and the content of the file.  On the server side the file that
        #JT was created would look similar to upload2.txthello world 2?test file?
        time.sleep(1)
        f = open(self.uploadPath+"/"+fileName,'rb')
        l = f.read(1024) # each time we only send 1024 bytes of data
        while (l):
            mySocket.send(l)
            l = f.read(1024)
        mySocket.close

    # Main logic of the clien, start the client application
    #JT - Updated main logic for new options to list upload files (option 2) and upload to server (option 4). 
    #JT - Updated option 1 to allways get the file list
    def start(self):
        opt=0
        while opt!=5:
            opt=self.getUserSelection()
            if opt==1:
                self.getFileList()
                self.printFileList()  
            elif opt==2:
                self.getLocalFileList()
                self.printLocalFileList()
            elif opt==3:
                self.downloadFile(self.selectDownloadFile())
            elif opt==4:
                self.uploadFile(self.selectUploadFile())
            else:
                pass
                
def main():
    c=client()
    c.start()
main()
