#!/usr/bin/env python3
import os
import socket
from cryptography.fernet import Fernet

HOST = "127.0.0.1"
PORT = 9001
KEY_FILE = "secret.key"

def load_or_create_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    with open(KEY_FILE, "rb") as f:
        return f.read().strip()

def run_server():
    key = load_or_create_key()
    cipher = Fernet(key)
    
    print("=" * 60)
    print("[Server] Initializing Symmetric Encryption Server (AES-128-CBC + HMAC)")
    print(f"[Server] Shared Symmetric Key: {key.decode('utf-8')}")
    print("=" * 60)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[Server] Listening on {HOST}:{PORT}...")
        
        conn, addr = s.accept()
        with conn:
            print(f"[Server] Connected by client at {addr}")
            
            # 1. Receive encrypted ciphertext from client
            encrypted_data = conn.recv(4096)
            if encrypted_data:
                print("\n--- [Server] Processing Incoming Message ---")
                print(f"[Server] Received ENCRYPTED data over network (Ciphertext):")
                print(f"  {encrypted_data.decode('utf-8')}")
                
                # 2. Decrypt message using symmetric key
                decrypted_bytes = cipher.decrypt(encrypted_data)
                actual_message = decrypted_bytes.decode("utf-8")
                print(f"[Server] Decrypted ACTUAL message using Symmetric Key:")
                print(f"  '{actual_message}'")
                
                # 3. Prepare server reply
                reply_plain = f"ACK from Server: Successfully decrypted your secret message: [{actual_message}]"
                print("\n--- [Server] Preparing Response ---")
                print(f"[Server] ACTUAL reply message:")
                print(f"  '{reply_plain}'")
                
                # 4. Encrypt reply using symmetric key
                encrypted_reply = cipher.encrypt(reply_plain.encode("utf-8"))
                print(f"[Server] ENCRYPTED reply data sent over network (Ciphertext):")
                print(f"  {encrypted_reply.decode('utf-8')}")
                
                # 5. Send encrypted reply to client
                conn.sendall(encrypted_reply)
                
        print("\n[Server] Connection handled. Shutting down server.")

if __name__ == "__main__":
    run_server()
