#!/usr/bin/env python3
import os
import socket
import ssl
import subprocess

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

HOST = "127.0.0.1"
PORT = 9002
SERVER_HOSTNAME = "localhost"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_FILE = os.path.join(BASE_DIR, "server.crt")
GEN_SCRIPT = os.path.join(BASE_DIR, "generate_certs.sh")

def ensure_certificates():
    if not os.path.exists(CERT_FILE):
        print(f"{CYAN}[Client]{RESET} {YELLOW}Server certificate not found. Generating...{RESET}")
        subprocess.run(["bash", GEN_SCRIPT], check=True)

def run_client():
    ensure_certificates()
    
    # Configure SSL Context for Client
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # Trust the server's certificate / CA
    context.load_verify_locations(cafile=CERT_FILE)
    
    print(f"{CYAN}======================================================================{RESET}")
    print(f"{CYAN}{BOLD}[Client] Starting SSL/TLS Secure Client{RESET}")
    print(f"{CYAN}[Client] Target: {YELLOW}{SERVER_HOSTNAME} ({HOST}:{PORT}){RESET}")
    print(f"{CYAN}[Client] Verifying Server with CA/Cert: {MAGENTA}{CERT_FILE}{RESET}")
    print(f"{CYAN}======================================================================{RESET}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as raw_sock:
        print(f"{CYAN}{BOLD}[Client]{RESET} Connecting to {YELLOW}{HOST}:{PORT}{RESET}...")
        raw_sock.connect((HOST, PORT))
        print(f"{CYAN}{BOLD}[Client]{RESET} TCP connection established. {GREEN}Initiating TLS Handshake...{RESET}")
        
        # Wrap the socket with SSL/TLS and authenticate server
        with context.wrap_socket(raw_sock, server_hostname=SERVER_HOSTNAME) as ssl_sock:
            print(f"\n{CYAN}--- [Client] TLS Handshake Successful ---{RESET}")
            print(f"{CYAN}{BOLD}[Client]{RESET} TLS Protocol Version : {GREEN}{BOLD}{ssl_sock.version()}{RESET}")
            cipher_info = ssl_sock.cipher()
            print(f"{CYAN}{BOLD}[Client]{RESET} Negotiated Cipher    : {MAGENTA}{BOLD}{cipher_info[0]}{RESET} ({cipher_info[1]}, {cipher_info[2]} bits)")
            peer_cert = ssl_sock.getpeercert()
            print(f"{CYAN}{BOLD}[Client]{RESET} Verified Server Cert Subject : {CYAN}{peer_cert.get('subject', ())}{RESET}")
            
            # Send secure message over TLS socket
            message = "Hello Server! This message is transmitted securely inside an encrypted SSL/TLS tunnel."
            print(f"\n{CYAN}--- [Client] Transmitting Secure Data ---{RESET}")
            print(f"{CYAN}{BOLD}[Client]{RESET} Sending message over {GREEN}{BOLD}SSL/TLS{RESET}:")
            print(f"  {YELLOW}'{message}'{RESET}")
            ssl_sock.sendall(message.encode("utf-8"))
            
            # Receive secure reply from server
            response_bytes = ssl_sock.recv(1024)
            reply = response_bytes.decode("utf-8")
            print(f"\n{CYAN}--- [Client] Receiving Secure Reply ---{RESET}")
            print(f"{CYAN}{BOLD}[Client]{RESET} Received reply over {GREEN}{BOLD}SSL/TLS{RESET}:")
            print(f"  {GREEN}'{reply}'{RESET}")
            
        print(f"\n{CYAN}{BOLD}[Client]{RESET} {GREEN}SSL connection closed cleanly. Secure transfer complete!{RESET}")

if __name__ == "__main__":
    run_client()
