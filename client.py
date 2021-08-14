'''
File: TCP/client.py
Brief: A program to create a client to connect to the server of the chatroom and receive and send messages using TCP
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


# Input client's name for future references
name = input("Enter your name: ")
print('\nType \'EXIT\' to leave the room(in all caps)\n\n')     # Exiting Instructions


# try and except block to create socket and if failed print the error message.
try: 
    # creating a socket object
    # AF_INET refers to the address family ipv4
    # SOCK_STREAM means the connection oriented TCP 
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print ("Socket successfully created")
    
except socket.error as err: 
    # if error is encountered printing the error
    print ("socket creation failed with error %s" %(err))
      
      
#Server is running on localhost and port 6000
# getting local host
host = socket.gethostname()
# defining port to be 6000 
port = 6000          

# connecting to the server running at localhost and port 6000     
client.connect((host,port))


def receiveMessage():
    '''
    A function to receive messages from server and print the message on the console
    An infinite loop is running to receive messages
    Also Handles sending the name of the client at apropriate time
    '''
    while True:
        # try and except block to receive message and print to console and
        # if there is error in receiving close the connection
        try:
            # calling recv method and saving the message in message variable after decoding
            message = client.recv(1024).decode('ascii')
            # if else block
            # checking if the sent messsage is "Name" or not
            if message == "Name":
                # if name
                # send the name to the server
                client.send(name.encode('ascii'))
            else:
                # if not
                # print the current message
                print(message)
        except :
            # if encountered error while receiving
            print("Connection to the Server is closed...\nBye...\n")
            # closing the connection
            client.close()
            # breaking the loop
            break

def sendMessage():
    '''
    A function to send messages to the server in a particular format
    An infinite loop is running to send the messages
    Also Handles exiting and closing the connection
    '''
    while True:
        # waiting for input and saving it in message with the {name}: as prefix
        message = f'\n{name}: {input("")}'
        # if block
        # checking if user typed "EXIT"
        if message == f'\n{name}: EXIT':
            # if true
            # close the connection
            client.close()
            # break the loop
            break
        # send the message to the server after encoding
        client.send(message.encode('ascii'))

'''
Defining two threads for receiving and sending function so that
it can run simultaneously and can be in ready mode to do both
'''
# defining receive_thread with target function as receiveMessage
receive_thread = threading.Thread(target=receiveMessage)
# starting the thread
receive_thread.start()

# defining send_thread with target function as sendMessage
send_thread = threading.Thread(target=sendMessage)
# starting the thread
send_thread.start()

