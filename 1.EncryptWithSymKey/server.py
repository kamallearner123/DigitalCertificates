#!/usr/bin/env python3
import os
import socket
from cryptography.fernet import Fernet

# ANSI Color Codes
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

HOST = "127.0.0.1"
PORT = 9001
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(BASE_DIR, "secret.key")

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
    
    print(f"{BLUE}======================================================================{RESET}")
    print(f"{BLUE}{BOLD}[Server] Initializing Symmetric Encryption Server (AES-128-CBC + HMAC){RESET}")
    print(f"{BLUE}[Server] Shared Symmetric Key: {MAGENTA}{BOLD}{key.decode('utf-8')}{RESET}")
    print(f"{BLUE}======================================================================{RESET}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"{BLUE}{BOLD}[Server]{RESET} Listening on {CYAN}{HOST}:{PORT}{RESET}...")
        
        conn, addr = s.accept()
        with conn:
            print(f"{BLUE}{BOLD}[Server]{RESET} Connected by client at {CYAN}{addr}{RESET}")
            
            # 1. Receive encrypted ciphertext from client
            encrypted_data = conn.recv(4096)
            if encrypted_data:
                print(f"\n{CYAN}--- [Server] Processing Incoming Message ---{RESET}")
                print(f"{BLUE}{BOLD}[Server]{RESET} {RED}{BOLD}ENCRYPTED Data Received over Network (Ciphertext):{RESET}")
                print(f"  {RED}{encrypted_data.decode('utf-8')}{RESET}")
                
                # 2. Decrypt message using symmetric key
                decrypted_bytes = cipher.decrypt(encrypted_data)
                actual_message = decrypted_bytes.decode("utf-8")
                print(f"{BLUE}{BOLD}[Server]{RESET} {GREEN}{BOLD}Decrypted ACTUAL Message using Symmetric Key:{RESET}")
                print(f"  {GREEN}'{actual_message}'{RESET}")
                
                # 3. Prepare server reply
                reply_plain = f"ACK from Server: Successfully decrypted your secret message: [{actual_message}]"
                print(f"\n{CYAN}--- [Server] Preparing Response ---{RESET}")
                print(f"{BLUE}{BOLD}[Server]{RESET} {YELLOW}{BOLD}ACTUAL Reply Message:{RESET}")
                print(f"  {YELLOW}'{reply_plain}'{RESET}")
                
                # 4. Encrypt reply using symmetric key
                encrypted_reply = cipher.encrypt(reply_plain.encode("utf-8"))
                print(f"{BLUE}{BOLD}[Server]{RESET} {RED}{BOLD}ENCRYPTED Reply Data sent over Network (Ciphertext):{RESET}")
                print(f"  {RED}{encrypted_reply.decode('utf-8')}{RESET}")
                
                # 5. Send encrypted reply to client
                conn.sendall(encrypted_reply)
                
        print(f"\n{BLUE}{BOLD}[Server]{RESET} Connection handled. Shutting down server.")

if __name__ == "__main__":
    run_server()
