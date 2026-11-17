# Secure Communications Lab: Digital Certificates & Cryptography

This repository demonstrates three progressive communication layers between a client and a server using Python and bash automation:

1. **`0.PlainText`** - Basic TCP socket communication exchanging unencrypted plain text data.
2. **`1.EncryptWithSymKey`** - Application-layer symmetric encryption (AES-128-CBC + HMAC-SHA256 via Fernet), displaying both the original plaintext and the encrypted ciphertext on both client and server sides.
3. **`2.UsingSSL`** - Transport-layer security (TLS 1.3 / SSL) using X.509 digital certificates and TLS handshakes, with cipher suite inspection and full certificate verification.

---

## Directory Structure

```
.
├── 0.PlainText/
│   ├── server.py       # TCP Server listening on port 9000
│   ├── client.py       # TCP Client sending plaintext data
│   └── start.sh        # Automates server backgrounding, client run, and shutdown
├── 1.EncryptWithSymKey/
│   ├── server.py       # Server decrypts incoming ciphertext and encrypts reply
│   ├── client.py       # Client encrypts payload and decrypts server response
│   ├── secret.key      # Pre-shared symmetric key (AES / Fernet)
│   └── start.sh        # Generates key (if missing) and runs client & server
├── 2.UsingSSL/
│   ├── generate_certs.sh # Generates self-signed X.509 cert & RSA key via OpenSSL
│   ├── server.crt      # X.509 Certificate with SAN (localhost, 127.0.0.1)
│   ├── server.key      # RSA private key
│   ├── server.py       # TLS Server (ssl.PROTOCOL_TLS_SERVER) on port 9002
│   ├── client.py       # TLS Client (ssl.PROTOCOL_TLS_CLIENT) verifying server cert
│   └── start.sh        # Automates cert generation and SSL client/server execution
├── .gitignore
└── README.md
```

---

## How to Run

### 0. PlainText Communication
```bash
cd 0.PlainText
./start.sh
```

### 1. Symmetric Key Encryption
```bash
cd 1.EncryptWithSymKey
./start.sh
```
*Both client and server print:*
- Shared symmetric key
- Actual plaintext message
- Encrypted ciphertext transmitted over the network

### 2. SSL/TLS Secure Connection
```bash
cd 2.UsingSSL
./start.sh
```
*Displays:*
- Generation of self-signed certificate and key
- Successful TLS handshake
- TLS protocol version (TLSv1.3)
- Negotiated cipher suite (e.g., `TLS_AES_256_GCM_SHA384`)
- Verified certificate details
- Secure bidirectional transmission
