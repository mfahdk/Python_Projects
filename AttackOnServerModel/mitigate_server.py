import socket
import os
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Shared secret key (16 bytes for AES-128)
K_AB = b'ThisIsA16ByteKey'
HOST = '127.0.0.1'
PORT = 9999

def encrypt(key, plaintext):
    #Encrypt plaintext using AES with ECB mode
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, 16))

def decrypt(key, ciphertext):
    #Decrypt ciphertext using AES with ECB mode
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)

#Function to handle each connection via threads
def handle_connection(conn, addr):
    try:
        print(f"[Bob] Connected by {addr}")

        # 1. Receive "I am Alice" and R_A from Alice
        data = conn.recv(1024)
        print("\n       I'm Alice, Ra  ")
        print("Alice ----------------> Bob")
        if not data:
            print("[Bob] No data received from client.")
            return

        parts = data.split(b'|')
        if len(parts) != 2:
            print("[Bob] Invalid message format from Alice.")
            return

        identity = parts[0].decode('utf-8')
        identity = identity.split(" ")[2]
        R_A = parts[1]
        print(f"[Bob] Received identity: {identity}, R_A = {R_A}")

        # 2. Generate R_B and send R_B along with E('Bob',R_A)
        R_B = os.urandom(16)  # 16-byte random nonce
        encrypted_R_A = encrypt(K_AB, R_A)
        encrypted_identity = encrypt(K_AB,b'Bob')
        message_to_alice = R_B + b'|' + encrypted_identity + b'|' + encrypted_R_A
        conn.sendall(message_to_alice)
        print("\n     Rb, E('Bob'Ra,Kab)  ")
        print("Alice <---------------- Bob")
        print(f"[Bob] Sent R_B and E('Bob'R_A). R_B = {R_B}")

        # 3. Receive E('Alice',R_B) from Alice
        data = conn.recv(1024)
        parts = data.split(b'|')

        print("\n    E('Alice'Rb,Kab)  ")
        print("Alice ----------------> Bob")
        if not data:
            return  # Exit current thread to allow handling of new session

        parts = data.split(b'|')
        decrypted_R_B = decrypt(K_AB, parts[1])
        decrypted_identity = decrypt(K_AB,parts[0])
        decrypted_identity = decrypted_identity.decode('utf-8')
        print(f"[Bob] Decrypted R_B from Alice: {decrypted_R_B}")
        print(f"[Bob] Recieved identity - {decrypted_identity}\n")

        if decrypted_identity == identity:
            print("[Bob] Authentication successful! (Alice verified)")
            conn.sendall(b"AUTH OK")
            return

        else:
            print("[Bob] Authentication failed! Wrong Identity.")
            conn.sendall(b"AUTH FAIL")
            return

    except Exception as e:
        print(f"[Bob] Error: {e}")
    finally:
        conn.close()
        print(f"[Bob] Connection with {addr} closed.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[Bob] Listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server_socket.accept()
        # Handle the current connection in a new thread
        threading.Thread(target=handle_connection, args=(conn, addr)).start()
        print("\nNEW CONNECTION")

if __name__ == "__main__":
    main()

