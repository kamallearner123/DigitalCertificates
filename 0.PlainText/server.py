#!/usr/bin/env python3
import socket

HOST = "127.0.0.1"
PORT = 9000

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[Server] Listening on {HOST}:{PORT} (Plain TCP)...")
        conn, addr = s.accept()
        with conn:
            print(f"[Server] Connection established with client at {addr}")
            data = conn.recv(1024)
            if data:
                message = data.decode("utf-8")
                print(f"[Server] Received plaintext message:\n  -> '{message}'")
                
                reply = f"ACK: Plaintext received successfully ('{message}')"
                conn.sendall(reply.encode("utf-8"))
                print(f"[Server] Sent plaintext reply:\n  -> '{reply}'")
        print("[Server] Closed connection and shutting down.")

if __name__ == "__main__":
    run_server()
