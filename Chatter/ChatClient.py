#********************************************
# chatClient.py
# Client program for chat application
# Created by:   Seth Lambert
# Created on:   4/08/18
# **Uses code from Jianzhen Zhou
#*********************************************
from socket import *

#Create a socket and connect to the server
serverName = "127.0.0.1" #Use IP address of server
serverPort = 12009
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

print("Connection successful, ready to communicate")
#Client send a Hello message to the server
clientSocket.send("Hello\t\t".encode())
#Check the response, if it asks for name, ask
# user to input the name and attempt to login to the server
#print(responseToHello.upper())
print("Welcome to the chat.")
while 1:
    request = clientSocket.recv(1024).decode('ascii')
    call = request.split('>')[0].strip()
    #print(call)
    if(call == "GET"):    
        method = request.split('>')[1].strip()
        message = request.split('>')[2].strip()

        if(method == "STATUS"):
            choice = input("Enter 1 for existing user, 2 for new User.")
            if(choice == "1"):
                status = "EX_USER\t\t"
                clientSocket.send(status.encode())
            elif(choice == "2"):
                status = "NEW_USER\t\t"
                clientSocket.send(status.encode())
            else:
                status = "HELLO\t\t"
                clientSocket.send(status.encode())
                
        #creating a new Username
        if(method == "USER"):
            username = "USER \t" + input("Username: ")
            username = (username + "\t\t")
            clientSocket.send(username.encode())

        elif(method == "NAME"):
            firstName = input("First Name: ")
            lastName = input("Last Name: ")
            fullName = ("NAME \t" + firstName + " " + lastName + "\t\t")
            clientSocket.send(fullName.encode())

        elif(method == "EMAIL"):
            email = "EMAIL \t" + input("Email: ")
            email = (email + "\t\t")
            clientSocket.send(email.encode())

        elif(method == "PASSWORD"):
            password = "PASSWORD \t" + input("Password (6 or more characters): ")
            password = (password + "\t\t")
            clientSocket.send(password.encode())

        elif(method == "LOGIN"):
            cont = input("Would you like to login now? [Y/N]: ")
            if(cont.upper() == 'Y'):
                status = "EX_USER\t\t"
                clientSocket.send(status.encode())
            elif(cont.upper() == 'N'):
                response = "QUIT\t\t"
                print("goodbye")
                clientSocket.send(response.encode())
                clientSocket.close()
                break
            else:
                print("input not recognized. goodbye.")
                response = "QUIT\t\t"
                clientSocket.send(response.encode())
                clientSocket.close()
                break

        #logging in
        elif(method == "USERNAME"):
            username = "USERNAME \t" + input("Username: ")
            username = (username + "\t\t")
            clientSocket.send(username.encode())
        elif(method == "PASS_LOG"):
            password = "PASS_LOG \t" + input("Password: ")
            password = (password + "\t\t")
            clientSocket.send(password.encode())
        elif(method == "SUCCESS"):
            request = "ACTIVE_USERS\t\t"
            clientSocket.send(request.encode())

        #start chat
        elif(method == "START_CHAT"):
            if ( len(message) < 2 ):
                #print("waiting for friends")
                request = "ACTIVE_USERS\t\t"
                clientSocket.send(request.encode())
            else:
                friend = input("Choose a friend who is active, if no friends are active, wait.\n" + message)
                request = ("FRIEND\t"+ friend.upper() + "\t\t")
                clientSocket.send(request.encode())
            
        #messaging
        elif(method == "SEND"):
            messageBody = input(username.upper() + ": ")
            if (messageBody == "LOGOUT"):
                awayMessage = input("Set away message: ")
                request = ("LOGOUT\t" + awayMessage + "\t\t")
                clientSocket.send(request.encode())
                clientSocket.close()
            else:
                request = ("SEND\t" + messageBody +"\t\t")
                clientSocket.send(request.encode())
        elif(method == "RECEIVE"):
            print(message)
            request = ("RECEIVE\t\t")
            clientSocket.send(request.encode())
                        
#if while loop breaks
clientSocket.close()
