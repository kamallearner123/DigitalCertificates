#!/usr/bin/env python3
import os
import socket
import ssl
import subprocess

HOST = "127.0.0.1"
PORT = 9002
SERVER_HOSTNAME = "localhost"
CERT_FILE = "server.crt"

def ensure_certificates():
    if not os.path.exists(CERT_FILE):
        print("[Client] Server certificate not found. Generating...")
        subprocess.run(["bash", "generate_certs.sh"], check=True)

def run_client():
    ensure_certificates()
    
    # Configure SSL Context for Client
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # Trust the server's certificate / CA
    context.load_verify_locations(cafile=CERT_FILE)
    
    print("=" * 60)
    print("[Client] Starting SSL/TLS Secure Client")
    print(f"[Client] Target: {SERVER_HOSTNAME} ({HOST}:{PORT})")
    print(f"[Client] Verifying Server with CA/Cert: {CERT_FILE}")
    print("=" * 60)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as raw_sock:
        print(f"[Client] Connecting to {HOST}:{PORT}...")
        raw_sock.connect((HOST, PORT))
        print("[Client] TCP connection established. Initiating TLS Handshake...")
        
        # Wrap the socket with SSL/TLS and authenticate server
        with context.wrap_socket(raw_sock, server_hostname=SERVER_HOSTNAME) as ssl_sock:
            print("\n--- [Client] TLS Handshake Successful ---")
            print(f"[Client] TLS Protocol Version : {ssl_sock.version()}")
            cipher_info = ssl_sock.cipher()
            print(f"[Client] Negotiated Cipher    : {cipher_info[0]} ({cipher_info[1]}, {cipher_info[2]} bits)")
            peer_cert = ssl_sock.getpeercert()
            print(f"[Client] Verified Server Cert Subject : {peer_cert.get('subject', ())}")
            
            # Send secure message over TLS socket
            message = "Hello Server! This message is transmitted securely inside an encrypted SSL/TLS tunnel."
            print("\n--- [Client] Transmitting Secure Data ---")
            print(f"[Client] Sending message over SSL/TLS:")
            print(f"  '{message}'")
            ssl_sock.sendall(message.encode("utf-8"))
            
            # Receive secure reply from server
            response_bytes = ssl_sock.recv(1024)
            reply = response_bytes.decode("utf-8")
            print("\n--- [Client] Receiving Secure Reply ---")
            print(f"[Client] Received reply over SSL/TLS:")
            print(f"  '{reply}'")
            
        print("\n[Client] SSL connection closed cleanly. Secure transfer complete!")

if __name__ == "__main__":
    run_client()
