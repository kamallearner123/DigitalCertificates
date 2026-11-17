#!/usr/bin/env python3
import socket

HOST = "127.0.0.1"
PORT = 9000

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[Client] Connecting to server at {HOST}:{PORT}...")
        s.connect((HOST, PORT))
        print("[Client] Connected!")
        
        message = "Hello Server! This is an unencrypted plain text message over TCP."
        print(f"[Client] Sending plaintext message:\n  -> '{message}'")
        s.sendall(message.encode("utf-8"))
        
        data = s.recv(1024)
        reply = data.decode("utf-8")
        print(f"[Client] Received plaintext reply from server:\n  -> '{reply}'")
        print("[Client] Data exchange complete.")

if __name__ == "__main__":
    run_client()
