#!/usr/bin/env python3
import socket

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

HOST = "127.0.0.1"
PORT = 9000

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"{CYAN}{BOLD}[Client]{RESET} Connecting to server at {YELLOW}{HOST}:{PORT}{RESET}...")
        s.connect((HOST, PORT))
        print(f"{CYAN}{BOLD}[Client]{RESET} {GREEN}Connected!{RESET}")
        
        message = "Hello Server! This is an unencrypted plain text message over TCP."
        print(f"{CYAN}{BOLD}[Client]{RESET} Sending plaintext message:\n  {YELLOW}↳ '{message}'{RESET}")
        s.sendall(message.encode("utf-8"))
        
        data = s.recv(1024)
        reply = data.decode("utf-8")
        print(f"{CYAN}{BOLD}[Client]{RESET} Received plaintext reply from server:\n  {GREEN}↳ '{reply}'{RESET}")
        print(f"{CYAN}{BOLD}[Client]{RESET} {GREEN}Data exchange complete.{RESET}")

if __name__ == "__main__":
    run_client()
