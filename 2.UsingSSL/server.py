#!/usr/bin/env python3
import os
import socket
import ssl
import subprocess

# ANSI Color Codes
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

HOST = "127.0.0.1"
PORT = 9002
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_FILE = os.path.join(BASE_DIR, "server.crt")
KEY_FILE = os.path.join(BASE_DIR, "server.key")
GEN_SCRIPT = os.path.join(BASE_DIR, "generate_certs.sh")

def ensure_certificates():
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print(f"{BLUE}[Server]{RESET} {YELLOW}Certificates not found. Generating self-signed SSL certificate...{RESET}")
        subprocess.run(["bash", GEN_SCRIPT], check=True)

def run_server():
    ensure_certificates()
    
    # Configure SSL Context for Server
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    
    print(f"{BLUE}======================================================================{RESET}")
    print(f"{BLUE}{BOLD}[Server] Starting SSL/TLS Secure Server{RESET}")
    print(f"{BLUE}[Server] Bound to {CYAN}{HOST}:{PORT}{RESET}")
    print(f"{BLUE}[Server] Using Certificate: {MAGENTA}{CERT_FILE}{RESET}")
    print(f"{BLUE}======================================================================{RESET}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as raw_sock:
        raw_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        raw_sock.bind((HOST, PORT))
        raw_sock.listen(1)
        print(f"{BLUE}{BOLD}[Server]{RESET} Listening on {CYAN}{HOST}:{PORT}{RESET} (waiting for TLS handshake)...")
        
        raw_conn, addr = raw_sock.accept()
        print(f"{BLUE}{BOLD}[Server]{RESET} Accepted TCP connection from {CYAN}{addr}{RESET}")
        
        # Wrap the socket with SSL/TLS
        with context.wrap_socket(raw_conn, server_side=True) as ssl_conn:
            print(f"\n{CYAN}--- [Server] TLS Handshake Established ---{RESET}")
            print(f"{BLUE}{BOLD}[Server]{RESET} TLS Protocol Version : {GREEN}{BOLD}{ssl_conn.version()}{RESET}")
            cipher_info = ssl_conn.cipher()
            print(f"{BLUE}{BOLD}[Server]{RESET} Negotiated Cipher    : {MAGENTA}{BOLD}{cipher_info[0]}{RESET} ({cipher_info[1]}, {cipher_info[2]} bits)")
            print(f"{BLUE}{BOLD}[Server]{RESET} Compression          : {ssl_conn.compression()}")
            
            # Receive secure data over TLS tunnel
            data = ssl_conn.recv(1024)
            if data:
                message = data.decode("utf-8")
                print(f"\n{CYAN}--- [Server] Processing Secure Incoming Data ---{RESET}")
                print(f"{BLUE}{BOLD}[Server]{RESET} Received message over {GREEN}{BOLD}SSL/TLS tunnel{RESET}:")
                print(f"  {YELLOW}'{message}'{RESET}")
                
                # Send secure reply
                reply = f"ACK over SSL/TLS: Server successfully received '{message}' via {ssl_conn.version()}!"
                ssl_conn.sendall(reply.encode("utf-8"))
                print(f"{BLUE}{BOLD}[Server]{RESET} Sent response over {GREEN}{BOLD}SSL/TLS tunnel{RESET}:")
                print(f"  {GREEN}'{reply}'{RESET}")
                
        print(f"\n{BLUE}{BOLD}[Server]{RESET} SSL connection closed cleanly. Server exiting.")

if __name__ == "__main__":
    run_server()
