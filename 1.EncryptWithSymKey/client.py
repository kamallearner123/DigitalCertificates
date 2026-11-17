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

def run_client():
    key = load_or_create_key()
    cipher = Fernet(key)
    
    print(f"{CYAN}======================================================================{RESET}")
    print(f"{CYAN}{BOLD}[Client] Initializing Symmetric Encryption Client{RESET}")
    print(f"{CYAN}[Client] Shared Symmetric Key: {MAGENTA}{BOLD}{key.decode('utf-8')}{RESET}")
    print(f"{CYAN}======================================================================{RESET}")
    
    # 1. Plaintext message to send
    actual_message = "Confidential Report: Authentication Token = XYZ-98765-SECRET"
    print(f"\n{CYAN}--- [Client] Preparing Outgoing Message ---{RESET}")
    print(f"{CYAN}{BOLD}[Client]{RESET} {GREEN}{BOLD}ACTUAL Message before Encryption:{RESET}")
    print(f"  {GREEN}'{actual_message}'{RESET}")
    
    # 2. Encrypt message using symmetric key
    encrypted_data = cipher.encrypt(actual_message.encode("utf-8"))
    print(f"{CYAN}{BOLD}[Client]{RESET} {RED}{BOLD}ENCRYPTED Data to send over Network (Ciphertext):{RESET}")
    print(f"  {RED}{encrypted_data.decode('utf-8')}{RESET}")
    
    # 3. Transmit encrypted data over TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"\n{CYAN}{BOLD}[Client]{RESET} Connecting to server at {YELLOW}{HOST}:{PORT}{RESET}...")
        s.connect((HOST, PORT))
        print(f"{CYAN}{BOLD}[Client]{RESET} {GREEN}Connected! Transmitting encrypted payload...{RESET}")
        s.sendall(encrypted_data)
        
        # 4. Receive encrypted response from server
        encrypted_response = s.recv(4096)
        print(f"\n{CYAN}--- [Client] Processing Server Response ---{RESET}")
        print(f"{CYAN}{BOLD}[Client]{RESET} {RED}{BOLD}Received ENCRYPTED Reply Data over Network (Ciphertext):{RESET}")
        print(f"  {RED}{encrypted_response.decode('utf-8')}{RESET}")
        
        # 5. Decrypt server response using symmetric key
        decrypted_response = cipher.decrypt(encrypted_response).decode("utf-8")
        print(f"{CYAN}{BOLD}[Client]{RESET} {YELLOW}{BOLD}Decrypted ACTUAL Reply Message from Server:{RESET}")
        print(f"  {YELLOW}'{decrypted_response}'{RESET}")
        
    print(f"\n{CYAN}{BOLD}[Client]{RESET} {GREEN}Symmetric encryption exchange completed successfully!{RESET}")

if __name__ == "__main__":
    run_client()
