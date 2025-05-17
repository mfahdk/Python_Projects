import socket
import rsa
from cryptography.fernet import Fernet
import threading

server_address = ('localhost', 8000)
confirm_pac = b"('CC')"
session_pac = b"('SK')"
errorcode, desc = '',''
ExceptionEventPacket = ["EE", errorcode, desc]

class myThread(threading.Thread):   #class used for multi-threading
    def __init__(self,s):
        threading.Thread.__init__(self)
        self.clientsocket=s

    def run(self):
        self.handleClient()
    
    def handleClient(self): #Function which determines if client has chosen secure or unecure communication
        try:
            while True:
                sessionKey = "SessionKey"
                print('\nwaiting to receive message')
                data = clientsocket.recv(2024)
                print('received ',data.decode()," from ",host)
                data = convert(data.decode())
                if data[0] == "SS":
                    if data[3] == 0:
                        sent=clientsocket.send(confirm_pac)

                elif data[0] == "EC":
                    if data[1] == "DES":
                        sent=clientsocket.send(session_pac)
                        public_key_str = data[2]
                        pub_key = rsa.PublicKey.load_pkcs1(public_key_str.encode()) #Receives the client public key in the correct format
                        print("Public Key: ",pub_key)
                        encrypted_key = rsa.encrypt(sessionKey.encode(), pub_key)
                        sent=clientsocket.send(encrypted_key)
                        sent=clientsocket.send(confirm_pac)
                    else:
                        sent=clientsocket.send(confirm_pac)
                        
                elif data[0] == "IN":
                    secure = clientsocket.recv(2024)
                    messages = secure.split(b";")
                    isSecure = messages[0]
                    if isSecure == b"1":
                        Key = messages[1]
                        clientPublicKey = Fernet(Key)
                        message = recieveMessage(1,data,clientPublicKey)
                    else:
                        message = recieveMessage(0,data," ")
                    response = generateResponse(message)
                    sent=clientsocket.send(response.encode())
                    
                elif data[0] == "Close-Packet":
                    print("\nClosing phase initiated by client. Connection closed by ",host)
        
        except socket.error as e:
            ExceptionEventPacket[1] = "110"
            ExceptionEventPacket[2] = "Socket Error"
            sendPacket(ExceptionEventPacket)
        
        except TypeError as e:
            ExceptionEventPacket[1] = "210"
            ExceptionEventPacket[2] = "Attribute Error"
            sendPacket(ExceptionEventPacket)
            print(ExceptionEventPacket)

        except ConnectionError as e:
            ExceptionEventPacket[1] = "310"
            ExceptionEventPacket[2] = "Connection Error"
            sendPacket(ExceptionEventPacket)

        except TimeoutError as e:
            ExceptionEventPacket[1] = "410"
            ExceptionEventPacket[2] = "Timeout Error"
            sendPacket(ExceptionEventPacket)
            
def sendPacket(packet): #function to sendPacket the packet after encoding
    strpacket=str(packet)
    message = bytes(strpacket, 'utf-8')
    sent = clientsocket.send(message)
    
def recieveMessage(secure,data,clientPublicKey): #Processes encrypted messages
    if secure == 1:
        public_key_str = data[1]
        message = clientPublicKey.decrypt(public_key_str)
        return message.decode()
    else:
        message = str(data[1])
        return message
                
def generateResponse(message): #Processes client data and sends appropriate response packet
    greetings = ["hello", "good morning", "good evening"]
    if any(phrase in message.lower() for phrase in greetings):
        print("Greetings (packet-type: GR)")
        return "Greetings (packet-type: GR)"
    elif 'what' in message.lower():
        print("Information Response (packet-type: IR)")
        return "Information Response (packet-type: IR)"
    elif 'where' in message.lower():
        print("Location Response (packet-type: LR)")
        return "Location Response (packet-type: LR)"
    elif 'when' in message.lower():
        print("Time Response (packet-type: TR)")
        return "Time Response (packet-type: TR)"
    elif 'search' in message.lower():
        print("Google results: ...... (packet-type: RR)")
        return "Google results: ...... (packet-type: RR)"
    elif 'permission' in message.lower():
        print("Granting permission using auth. Credentials (packet-type: PR)")
        return "Granting permission using auth. Credentials (packet-type: PR)"
    else:
        print("Unknown request")
        return "Unkown request"

def convert(string):   #converts a string list into a list
    res = eval(string)
    return res

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8888
serversocket.bind((host, port))
serversocket.listen(5)

while True:
    clientsocket,addr = serversocket.accept()

    t1=myThread(clientsocket)
    t1.start()
