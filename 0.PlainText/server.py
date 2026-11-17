#!/usr/bin/env python3
import socket

# ANSI Color Codes
CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

HOST = "127.0.0.1"
PORT = 9000

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"{BLUE}{BOLD}[Server]{RESET} Listening on {CYAN}{HOST}:{PORT}{RESET} (Plain TCP)...")
        conn, addr = s.accept()
        with conn:
            print(f"{BLUE}{BOLD}[Server]{RESET} Connection established with client at {CYAN}{addr}{RESET}")
            data = conn.recv(1024)
            if data:
                message = data.decode("utf-8")
                print(f"{BLUE}{BOLD}[Server]{RESET} Received plaintext message:\n  {YELLOW}↳ '{message}'{RESET}")
                
                reply = f"ACK: Plaintext received successfully ('{message}')"
                conn.sendall(reply.encode("utf-8"))
                print(f"{BLUE}{BOLD}[Server]{RESET} Sent plaintext reply:\n  {GREEN}↳ '{reply}'{RESET}")
        print(f"{BLUE}{BOLD}[Server]{RESET} Closed connection and shutting down.")

if __name__ == "__main__":
    run_server()
