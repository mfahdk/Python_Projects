import socket
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

K_AB = b'ThisIsA16ByteKey'

def encrypt(key, plaintext):
    #Encrypt plaintext using AES with ECB mode
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, 16))

def decrypt(key, ciphertext):
    #Decrypt ciphertext using AES with ECB mode
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), 16)

def main():
    HOST = '127.0.0.1'
    PORT = 9999

    client_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_connection.connect((HOST, PORT))
    print(f"[Alice] Connected to (Bob) at {HOST}:{PORT}")

    # 1. Send "I am Alice" and R_A
    R_A = os.urandom(16)
    message = b"I am Alice |" + R_A
    client_connection.sendall(message)
    print("\n      I'm Alice, Ra  ")
    print("Alice ----------------> Bob")
    print(f"[Alice] Sent identity and R_A. R_A = {R_A}")

    # 2. Receive R_B and E("Bob",R_A) from Bob
    data = client_connection.recv(1024)
    print("\n     Rb, E('Bob',Ra,Kab)  ")
    print("Alice <---------------- Bob")
    if not data:
        print("[Alice] No response from Bob.")
        return

    parts = data.split(b'|')
    R_B = parts[0]
    decrypted_identity = decrypt(K_AB,parts[1])
    print(f"\n[Alice] Recieved identity - {decrypted_identity.decode('utf-8')}")

    # 3. Encrypt and send ('Alice',R_B) back to Bob
    encrypted_R_B = encrypt(K_AB, R_B)
    encrypted_identity = encrypt(K_AB,b'Alice')
    message = encrypted_identity + b'|' +encrypted_R_B
    client_connection.sendall(message)
    print("\n      E('Alice'Rb,Kab)  ")
    print("Alice ----------------> Bob")
    print("[Alice] Sent E(R_B). Waiting for authentication status...")

    # Receive final authentication status from Bob
    auth_status = client_connection.recv(1024)
    if auth_status == b"AUTH OK":
        print("[Alice] Bob authenticated successfully!")
    else:
        print("[Alice] Bob authentication failed.")

if __name__ == "__main__":
    main()

