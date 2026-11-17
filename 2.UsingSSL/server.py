#!/usr/bin/env python3
import os
import socket
import ssl
import subprocess

HOST = "127.0.0.1"
PORT = 9002
CERT_FILE = "server.crt"
KEY_FILE = "server.key"

def ensure_certificates():
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print("[Server] Certificates not found. Generating self-signed SSL certificate...")
        subprocess.run(["bash", "generate_certs.sh"], check=True)

def run_server():
    ensure_certificates()
    
    # Configure SSL Context for Server
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    
    print("=" * 60)
    print("[Server] Starting SSL/TLS Secure Server")
    print(f"[Server] Bound to {HOST}:{PORT}")
    print(f"[Server] Using Certificate: {CERT_FILE}")
    print("=" * 60)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as raw_sock:
        raw_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        raw_sock.bind((HOST, PORT))
        raw_sock.listen(1)
        print(f"[Server] Listening on {HOST}:{PORT} (waiting for TLS handshake)...")
        
        raw_conn, addr = raw_sock.accept()
        print(f"[Server] Accepted TCP connection from {addr}")
        
        # Wrap the socket with SSL/TLS
        with context.wrap_socket(raw_conn, server_side=True) as ssl_conn:
            print("\n--- [Server] TLS Handshake Established ---")
            print(f"[Server] TLS Protocol Version : {ssl_conn.version()}")
            cipher_info = ssl_conn.cipher()
            print(f"[Server] Negotiated Cipher    : {cipher_info[0]} ({cipher_info[1]}, {cipher_info[2]} bits)")
            print(f"[Server] Compression          : {ssl_conn.compression()}")
            
            # Receive secure data over TLS tunnel
            data = ssl_conn.recv(1024)
            if data:
                message = data.decode("utf-8")
                print("\n--- [Server] Processing Secure Incoming Data ---")
                print(f"[Server] Received message over SSL/TLS tunnel:")
                print(f"  '{message}'")
                
                # Send secure reply
                reply = f"ACK over SSL/TLS: Server successfully received '{message}' via {ssl_conn.version()}!"
                ssl_conn.sendall(reply.encode("utf-8"))
                print(f"[Server] Sent response over SSL/TLS tunnel:")
                print(f"  '{reply}'")
                
        print("\n[Server] SSL connection closed cleanly. Server exiting.")

if __name__ == "__main__":
    run_server()
