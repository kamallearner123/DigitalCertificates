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

def run_client():
    key = load_or_create_key()
    cipher = Fernet(key)
    
    print("=" * 60)
    print("[Client] Initializing Symmetric Encryption Client")
    print(f"[Client] Shared Symmetric Key: {key.decode('utf-8')}")
    print("=" * 60)
    
    # 1. Plaintext message to send
    actual_message = "Confidential Report: Authentication Token = XYZ-98765-SECRET"
    print("\n--- [Client] Preparing Outgoing Message ---")
    print(f"[Client] ACTUAL message before encryption:")
    print(f"  '{actual_message}'")
    
    # 2. Encrypt message using symmetric key
    encrypted_data = cipher.encrypt(actual_message.encode("utf-8"))
    print(f"[Client] ENCRYPTED data to send over network (Ciphertext):")
    print(f"  {encrypted_data.decode('utf-8')}")
    
    # 3. Transmit encrypted data over TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"\n[Client] Connecting to server at {HOST}:{PORT}...")
        s.connect((HOST, PORT))
        print("[Client] Connected! Transmitting encrypted payload...")
        s.sendall(encrypted_data)
        
        # 4. Receive encrypted response from server
        encrypted_response = s.recv(4096)
        print("\n--- [Client] Processing Server Response ---")
        print(f"[Client] Received ENCRYPTED reply data over network (Ciphertext):")
        print(f"  {encrypted_response.decode('utf-8')}")
        
        # 5. Decrypt server response using symmetric key
        decrypted_response = cipher.decrypt(encrypted_response).decode("utf-8")
        print(f"[Client] Decrypted ACTUAL reply message from Server:")
        print(f"  '{decrypted_response}'")
        
    print("\n[Client] Symmetric encryption exchange completed successfully!")

if __name__ == "__main__":
    run_client()
