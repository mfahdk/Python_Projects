import socket
import rsa
from cryptography.fernet import Fernet
import json

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
sever_address = socket.gethostbyname(host)
port = 8888

message1, message2 = "(SS,TTP,v1.0,0)", "(SS,TTP,v1.0,1)"
secure,auth,authID,sessionKey,message =  0, '', '','','' #initialize values in packet list
startPacket=["SS","TTP","v1.0",secure] #packet is a list with 4 values at all times
encryptionPacket = ["EC",auth,authID]
sessionPacket = ["SK",sessionKey]
informationPacket = ["IN",message]

key = Fernet.generate_key() #use fernet to create a key
clientPublicKey = Fernet(key)

publickey, privatekey = rsa.newkeys(200) #creates encryption key

username = "csec"
passwd = "python"

def exceptionHandle(ExceptionEventPacket): #Check if it's an error packet
    if ExceptionEventPacket[0] == "EE" or ExceptionEventPacket == "EE":  
        error_code = ExceptionEventPacket[1]
        description = ExceptionEventPacket[2]
        print("Recieved error",description," with error code : ",error_code)

def Message(): #Function to get input from user and process response from server
    msg = input("Enter your message: ")
    while msg.lower() != "end":
        msg = msg.lower()
        informationPacket[0] = "IN"
        informationPacket[1] = msg
        sendPacket(informationPacket)
        sent = sock.send(b"0")
        response = sock.recv(2024)
        exceptionHandle(response)
        print("Response from server: ",response.decode())
        msg = input("Enter your message: ")
    else:
        closeConnection()
        exit()
    
def encryptedMessage(): #Function used if secure communication is involved
    msg = input("Enter your message: ")
    while msg.lower() != "end":
        msg = msg.lower()
        informationPacket[0] = "IN"
        encryptMsg = clientPublicKey.encrypt(msg.encode())
        informationPacket[1] = encryptMsg
        sendPacket(informationPacket)
        combined_message = b"1" + b";" + key    #because of tcp message is sent combined
        sent = sock.send(combined_message)
        response = sock.recv(2024)
        exceptionHandle(response)
        print("Response from server: ",response.decode())
        msg = input("Enter your message: ")
    else:
        closeConnection()
        exit()

def sendPacket(packet): #Function to sendPacket the packet after encoding
    strpacket=str(packet)
    message = bytes(strpacket, 'utf-8')
    sent = sock.send(message)

def receive(): #Function to receive string data and convert to list format
    data = sock.recv(2024)
    res = data.decode()
    res1 = eval(res)
    exceptionHandle(res1)
    return res1

def closeConnection(): #Closes connection after client inputs "end"
    closePacket = ["Close-Packet"]  
    sendPacket(closePacket)  
    sock.close()
    print("Closing phase initiated. Connection closed.")        

sock.connect((host, port))
print("",message1,"\n",message2)
x = input("Choose an option 1 or 0: ")
if x == "0":
    startPacket[3] = 0
    sendPacket(startPacket)
    confirmation = receive()
    print ('received',confirmation)
    Message()
    
elif x == "1":
    startPacket[3] = 1
    sendPacket(startPacket)
    inp1 = input('Do you want encryption or authentication? Type e for encryption or a for authentication: ')
    
    if inp1.lower() == "e":
        pub_Key = publickey.save_pkcs1().decode()    #used to sendPacket client public key to the server in the PublicKey format
        encryptionPacket[1] = "DES"
        encryptionPacket[2] = pub_Key
        sendPacket(encryptionPacket)
        encryption = receive()
        print ('received',encryption)
        Key = sock.recv(2024)
        exceptionHandle(Key)
        sessionKey = rsa.decrypt(Key, privatekey).decode()
        sessionPacket[1] = sessionKey
        print(sessionPacket)
        confirmation = receive()
        print ('received',confirmation)
        encryptedMessage()
        print(informationPacket)
        
    elif inp1.lower() == "a":                       #checks if password and username match
        uname = input('Enter username : ')
        upass = input('Enter password : ')
        while username != uname and passwd != upass:
            print("Incorrect Username and/or Password, try again ")
            uname = input('Enter username : ')
            upass = input('Enter password : ')
        else:
            encryptionPacket[1] = 'Authentication'
            encryptionPacket[2] = uname +":"+ upass
            sendPacket(encryptionPacket)
            encryption = receive()
            print ('received',encryption)
            Message()
    else:
       print("Incorrect Option") 
else:
    print("Incorrect Option")
