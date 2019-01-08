#********************************************
# chatServer.py
# Server program for creating user accounts
# Created by:   Seth Lambert
# Created on:   3/12/18
# **Uses code from Jianzhen Zhou
#*********************************************
from socket import *
from datetime import datetime
from _thread import *

#Create a welcome socket bound at serverPort
serverPort = 12009
serverSocket = socket(AF_INET,SOCK_STREAM)
#serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('',serverPort))
serverSocket.listen(10)
print ('This server is ready to receive')
accessTime = datetime.now();
print("Access time is", accessTime);

def   greetingLogThread(connectionSocket):
    loginStatus = "Failure" # A client was not logged in when just connected

    #Wait for the hello message
    while 1:    #The loop allow processing of multiple login or report request from the same client
        request = connectionSocket.recv(1024).decode('ascii')
        print("Request message:", request)
        if(request.upper() == "QUIT"):
            break     #break the communication with this client

        methodName = request.split('\t')[0].strip()
        condition = request.split('\t')[1].strip()
        print("From", addr,methodName)
        
        #Ask for status if a hello message is received
        if(methodName.upper() == "HELLO"):
            response = "GET>STATUS>"
            connectionSocket.send(response.encode())

        #Repsond to status
        elif (methodName.upper() == "NEW_USER"):
            response = "GET>USER>"
            connectionSocket.send(response.encode())
        elif (methodName.upper() == "EX_USER"):
            response = "GET>USERNAME>"
            connectionSocket.send(response.encode())    

        #Receive and verify username
        elif(methodName.upper() == "USER"):
            userName = request.split('\t')[1].strip()
            print("Username received: " + userName + "...checking username")
            #Open the UserProfile file to check the username
            exists = "NO" #exists works like a boolean
            for line in open("UserProfile.txt", 'r'):
                registeredUser = line.split("\t")[0].strip()
                if( userName == registeredUser):
                    print("User already exists.")
                    response = "GET>USER>Username already exists>"
                    exists = "YES" #sets exists to true
                    connectionSocket.send(response.encode())
                    break   #Skip later records
            if(exists == "NO"): #creates new username
                print("username received, getting name") 
                response = "GET>NAME>"
                connectionSocket.send(response.encode())
                    
        #Receive and verify name
        elif(methodName.upper() == "NAME"):
            name = request.split('\t')[1].strip()
            print("Name received: " + name + "...checking name.")
            #Open the UserProfile file to check the name
            exists = "NO" #exists works like a boolean
            for line in open("UserProfile.txt", 'r'):
                registeredName = line.split("\t")[1].strip()
                if(name.upper() == registeredName.upper()):
                    print("User with this name already exist.")
                    response = "GET>NAME>User with this name already exists>"
                    exists = "YES" #sets exists to true
                    connectionSocket.send(response.encode())
                    break   #Skip later records
            if(exists == "NO"): #creates new username
                print("name received, getting email") 
                response = "GET>EMAIL>"
                connectionSocket.send(response.encode())

        #Receive and verify email
        elif(methodName.upper() == "EMAIL"):
            email = request.split('\t')[1].strip()
            print("Email received: " + name + "...checking email.")
            #Open the UserProfile file to check the name
            exists = "NO" #exists works like a boolean
            for line in open("UserProfile.txt", 'r'):
                registeredEmail = line.split("\t")[2].strip()
                if( email == registeredEmail):
                    print("User with this email already exists.")
                    response = "GET>EMAIL>User with this email already exists>"
                    exists = "YES" #sets exists to true
                    connectionSocket.send(response.encode())
                    break   #Skip later records
            if(exists == "NO"): #creates new username
                print("email received, getting password") 
                response = "GET>PASSWORD>"
                connectionSocket.send(response.encode())

        #Receive and verify password
        elif(methodName.upper() == "PASSWORD"):
            password = request.split('\t')[1].strip()
            print("Name received: " + name + "...checking password length.")
            if(len(password) < 6):
                print("Password must be longer than 6 characters.")
                response = "GET>PASSWORD>Password must be longer than 6 characters>"
                connectionSocket.send(response.encode())
            elif(len(password) > 6):
                log = (userName.upper() +"\t"+ name +"\t"+ email +"\t"+ password +"\n")
                print(log)
                logFile = open("UserProfile.txt", "a")
                logFile.write(log)
                logFile.close()
                print("log recorded")
                status = (userName +"\t"+ "NOT_ACTIVE" +"\t"+ "User not logged in"+"\n") 
                statusFile = open("UserStatus.txt", "a")
                statusFile.write(status)
                statusFile.close()
                response = "GET>LOGIN>"
                connectionSocket.send(response.encode())

        #login existing user
        elif(methodName.upper() == "EX_USER"):
            response = "GET>USERNAME>"
            connectionSocket.send(response.encode())
        elif(methodName.upper() == "USERNAME"):
            userName = request.split('\t')[1].strip()
            print("Username received: " + userName + "...checking username")
            #Open the UserProfile file to check the username
            exists = "NO" #exists works like a boolean
            for line in open("UserProfile.txt", 'r'):
                registeredUser = line.split("\t")[0].strip()
                if( userName.upper() == registeredUser):
                    print("User exists.")
                    response = "GET>PASS_LOG>"
                    exists = "YES" #sets exists to true
                    connectionSocket.send(response.encode())
                    break   #Skip later records
            if(exists == "NO"): #requests an existing username
                print("username failed") 
                response = "GET>USERNAME>"
                connectionSocket.send(response.encode())
        elif(methodName.upper() == "PASS_LOG"):
            password = request.split('\t')[1].strip()
            print("Password received: " + password + "...checking password")
            #Open the UserProfile file to check the password matches the usernam
            exists = "NO" #exists works like a boolean
            for line in open("UserProfile.txt", 'r'):
                registeredUser = line.split("\t")[0].strip()
                registeredPassword = line.split("\t")[3].strip()
                if( userName.upper() == registeredUser and password == registeredPassword ):
                    print("User exists.")
                    response = "GET>SUCCESS>"
                    exists = "YES" #sets exists to true
                    break   #Skip later records
            #mark current user active
            lines = open('UserStatus.txt').readlines()
            for i, line in enumerate(lines[:]):
                readUser = line.split("\t")[0].strip()
                if ( readUser == userName ):
                    status = (userName.upper() +"\t"+ "ACTIVE" +"\t"+ "User available"+"\n")
                    lines[i] = status
            with open('UserStatus.txt', 'w+') as file:
                file.truncate(0)
            file.close()
            open('UserStatus.txt', 'w').writelines(lines)
            #user is now logged in
            loginStatus = "Success"
            connectionSocket.send(response.encode())
            if(exists == "NO"): #requests another password
                print("password failed") 
                response = "GET>PASS_LOG>"
                connectionSocket.send(response.encode())

        #send active users
        elif(methodName.upper() == "ACTIVE_USERS"):
            #get friendslist to send
            friendsList = ""
            for line in open("UserStatus.txt", 'r'):
                checkUser = line.split("\t")[0].strip()
                checkStatus = line.split("\t")[1].strip()
                awayMessage = line.split("\t")[2].strip()
                userName = userName.upper()
                if ( checkUser.upper() != userName and checkStatus == "ACTIVE" ):
                    friendsList = (friendsList + checkUser +"\t"+ checkStatus +"\n")
                #if ( checkUser.upper() != userName and checkStatus == "NOT_ACTIVE" ):
                    #friendsList = (friendsList + checkUser +"\t"+ awayMessage +"\n")       
            response = ("GET>START_CHAT>" + friendsList +">")
            connectionSocket.send(response.encode())

        #confirm friend available
        elif(methodName.upper() == "FRIEND"):
            friend = condition
            for line in open("UserStatus.txt", 'r'):
                checkUser = line.split("\t")[0].strip()
                checkStatus = line.split("\t")[1].strip()
                print("check status of " + friend + " and " + checkUser)
                if ( friend == checkUser and checkStatus == "ACTIVE"):
                    response = "GET>SEND>"
                    break
                else:
                    response = "GET>SUCCESS>"
            connectionSocket.send(response.encode())
        
        #messaging
        elif(methodName.upper() == "SEND"): #adds message to message queue
            #TO: FROM: MESSAGE
            toQueue = (friend +"\t"+ userName.upper() +"\t"+ condition + "\n")
            queue = open("MessageQueue.txt", "a")
            queue.write(toQueue)
            queue.close()
            #check queue for messages
            message = ""
            linesQueue = open('MessageQueue.txt').readlines()
            for i, line in enumerate(linesQueue[:]):
                readUser = line.split("\t")[0].strip()
                readSender = line.split("\t")[1].strip()
                readMessage = line.split("\t")[2].strip()
                if ( readUser == userName ):
                    message = (message + readSender.upper() +": "+ readMessage + "\n")
                    del linesQueue[i]
            with open('MessageQueue.txt', 'w+') as file:
                file.truncate(0)
            file.close()
            open('MessageQueue.txt', 'w').writelines(linesQueue)
            response = ("GET>RECEIVE>" + message + ">")
            connectionSocket.send(response.encode())
        elif(methodName.upper() == "RECEIVE"): #removes message(s) from message queue and delivers
            response = "GET>SEND>"
            connectionSocket.send(response.encode())

        #set away message and quit
        elif(methodName.upper() == "LOGOUT"):
            reader = open('UserStatus.txt').readlines()
            for i, line in enumerate(reader[:]):
                readUser = line.split("\t")[0].strip()
                if ( readUser == userName ):
                    status = (userName +"\t"+ "NOT_ACTIVE" +"\t"+ condition +"\n")
                    reader[i] = status
            with open('UserStatus.txt', 'w+') as file:
                file.truncate(0)
            file.close()
            open('UserStatus.txt', 'w').writelines(reader)
            print("goodbye")
            connectionSocket.close()

            

    #if while loop breaks
    connectionSocket.close()

while 1:
    connectionSocket, addr = serverSocket.accept()
    print("from", addr)
    start_new_thread(greetingLogThread, (connectionSocket,))
