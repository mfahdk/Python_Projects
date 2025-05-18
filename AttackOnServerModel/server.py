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

        parts = data.split(b'|', 1)
        if len(parts) != 2:
            print("[Bob] Invalid message format from Alice.")
            return

        alice_identity = parts[0].decode('utf-8')
        R_A = parts[1]
        print(f"[Bob] Received identity: {alice_identity}, R_A = {R_A}")

        # 2. Generate R_B and send R_B along with E(R_A)
        R_B = os.urandom(16)  # 16-byte random nonce
        encrypted_R_A = encrypt(K_AB, R_A)
        message_to_alice = R_B + b'|' + encrypted_R_A
        conn.sendall(message_to_alice)
        print("\n       Rb, E(Ra,Kab)  ")
        print("Alice <---------------- Bob")
        print(f"[Bob] Sent R_B and E(R_A). R_B = {R_B}")

        # 3. Receive E(R_B) from Alice
        data = conn.recv(1024)
        print("\n       E(Rb,Kab)  ")
        print("Alice ----------------> Bob")
        if not data:
            return  # Exit current thread to allow handling of new session

        decrypted_R_B = decrypt(K_AB, data)
        print(f"[Bob] Decrypted R_B from Alice: {decrypted_R_B}")

        if decrypted_R_B == R_B:
            print("[Bob] Authentication successful! (Alice verified)")
            conn.sendall(b"AUTH OK")
            return

        else:
            print("[Bob] Authentication failed! Wrong R_B.")
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
