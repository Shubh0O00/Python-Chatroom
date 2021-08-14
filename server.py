'''
File: TCP/server.py
Brief: A program to create a server using sockets and handle multiple clients using TCP. It will act as a server for a chatroom.
Authors: BT19CSE119 SHUBHAM
         BT19CSE129 ANUJ
         BT19CSE094 YOGESH
         BT19CSE078 KRISHNA
         BT19CSE108 DUSHYANT
         BT19CSE122 ASTITVA
Date: 11/08/2021
'''
# importing socket module
import socket 

# importing threading module
import threading              

# try and except block to create socket and if failed print the error message.
try: 
    # creating a socket object
    # AF_INET refers to the address family ipv4
    # SOCK_STREAM means the connection oriented TCP
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print ("Socket successfully created")
    
except socket.error as err: 
    # if error is encountered printing the error
    print ("socket creation failed with error %s" %(err))

     
# getting the localhost to run the server   
host = socket.gethostname() 
# defining port to be 6000 
port = 6000      

# binding the server to defined host and port
server.bind((host, port))
print(f"Socket binded to {port}\n")

#listening for conections to the server.
server.listen()      
print("Server is listening...\n")

clients = []        #list to store ip and port of clients
names = []          #list to store name chosen by the clients

def brodcastToAll(message, current):
    '''
    A function to send the message to all the clients
    except the sender i.e. current client
    
    message: A decoded string contain message sent by client
    current: ip and port of the current client
    '''
    for client in clients:
        # iterating through the clients list
        if client != current:
            # except for the current client that is passed
            # send the message to the client
            client.send(message)

def clientHandling(client):
    '''
    A function to handle a client
    An infinite loop is running in the function waiting to receive message
    and will close the connection if nothing is received
    
    client: ip and port of the client
    '''
    while True:
        # try and except block to receive message and if no message is received
        # close the connection and remove the name and client from the lists
        try:
            # receive the message and saving it in message variable
            message = client.recv(1024)
            # calling the brodcastToAll function by passing message and client
            brodcastToAll(message, client)
        except :
            # finding the index of the client in clients list
            index = clients.index(client)
            # removing the client from clients list
            clients.remove(client)
            # closing the connection to the client
            client.close()
            # finding the index of the name in names list
            name = names[index]
            # calling the broadcastToAll function to print client left the chat
            brodcastToAll(f"\n{name} left the chat".encode('ascii'), client)
            # printing that client left the chat on the server console
            print(f"\n{name} left the chat\n")
            # removing the name from names list
            names.remove(name)
            # breaking from the loop
            break
        
                  
def receiveConnection():
    '''
    A function to receive connection
    An infinite loop is running in the function waiting to receive connection
    and add the name sent and client to the names and clients list
    '''
    while True:
        # calling accept() function to accept connections
        # and saving the client and address
        client, addr = server.accept()
        # printing the connection addr to console
        print(f"Connected with {str(addr)}\n")
        # sending "Name" to tell client program to send its name
        client.send("Name".encode('ascii'))
        
        # receiving the name and decoding it
        name = client.recv(1024).decode('ascii')
        # appending the name to names list
        names.append(name)
        # appending the client to clients list
        clients.append(client)
        
        # printing name of the client to the console
        print(f"Name of the client is: {name}")
        # calling brodcastToAll function telling all other client that current client has joined
        brodcastToAll(f"{name} joined the chat".encode('ascii'), client)
        # sending the client confirmation that it is connected to the server
        client.send("Connected to the server".encode('ascii'))
        
        # defining a thread with target function as clientHandling and passing the arguement client
        # this will create a different thread for every new client that joins the chat room
        thread = threading.Thread(target=clientHandling, args=(client,))
        # starting the thread
        thread.start()
                       
# calling the receiveConnection funtion to start the server as it is the entry point of the server
receiveConnection()