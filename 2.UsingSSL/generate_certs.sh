#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

# ANSI Colors
CYAN="\033[1;36m"
GREEN="\033[1;32m"
RESET="\033[0m"

echo -e "${CYAN}[generate_certs.sh] Generating self-signed X.509 SSL/TLS certificate and RSA private key...${RESET}"

openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout server.key \
    -out server.crt \
    -days 365 \
    -subj "/C=US/ST=CA/L=SanFrancisco/O=DevSec/OU=TLS/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

echo -e "${GREEN}[generate_certs.sh] Certificate (server.crt) and private key (server.key) created successfully.${RESET}"
