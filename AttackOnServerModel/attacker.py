import socket
import os
import threading

# Configuration
HOST = '127.0.0.1'
PORT = 9999

def main():
    #Start first connection
    first_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    first_connection.connect((HOST,PORT))

    print(f"[Trudy] Connected to (Bob) at {HOST}:{PORT}")

    # 1. Send "I am Alice" and R_A
    R_A = os.urandom(16)
    message = b"I am Alice |" + R_A
    first_connection.sendall(message)
    print("\n       I'm Alice, Ra  ")
    print("Trudy ----------------> Bob")
    print(f"[Trudy] Sent identity and R_A. R_A = {R_A}")

    # 2. Receive R_B and E(R_A) from Bob
    data = first_connection.recv(1024)
    print("\n        Rb, E(Ra,Kab)  ")
    print("Trudy <---------------- Bob")
    if not data:
        print("[Trudy] No response from Bob.")
        return

    parts = data.split(b'|', 1)
    R_B = parts[0]
    #Get Rb to send back to Bob in new connection
   
    #Start second session to get E(Rb,Kab)
    print("\nSECOND CONNECTION\n")
    #Start second connection
    second_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    second_connection.connect((HOST,PORT))

    print(f"[Trudy] Connected to (Bob) at {HOST}:{PORT}")

    # 3. Send "I am Trudy" and R_B
    message = b"I am Alice |" + R_B
    second_connection.sendall(message)
    print("\n       I'm Alice, Rb  ")
    print("Trudy ----------------> Bob")
    print(f"[Trudy] Sent identity and R_B. R_B = {R_B}")

    # 4. Receive R_B and E(R_A) from Bob
    data = second_connection.recv(1024)
    print("\n        Rc, E(Rb,Kab)  ")
    print("Trudy <---------------- Bob")
    if not data:
        print("[Trudy] No response from Bob.")
        return

    parts = data.split(b'|', 1)
    encrypted_R_B = parts[1]
    #Get encrypted Rb to send to bob in first connection
   
    print("\nBACK TO FIRST CONNECTION")
    # 5. Encrypt and send R_B back to Bob
    first_connection.sendall(encrypted_R_B)
    print("\n       E(Rb,Kab)  ")
    print("Trudy ----------------> Bob")
    print("[Trudy] Sent E(R_B). Waiting for authentication status...")

    # Receive final authentication status from Bob
    auth_status = first_connection.recv(1024)
    if auth_status == b"AUTH OK":
        print("[Trudy] Bob authenticated successfully!")
    else:
        print("[Trudy] Bob authentication failed.")

if __name__ == "__main__":
    main()

