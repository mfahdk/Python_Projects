# Secure Authentication Protocol Simulation

This project demonstrates a **challenge-response mutual authentication protocol** between two parties, `Alice` and `Bob`, with an emphasis on identifying vulnerabilities and implementing mitigations against **reflection attacks**. It includes attack simulation and enhanced protocol versions using AES encryption.

> **DISCLAIMER**
> This project is for **educational and ethical testing purposes only**. Do not use any part of this code against real systems without proper authorization.

---

## Project Structure

```bash
.
├── attacker.py              # Reflection attack simulation (Trudy)
├── client.py                # Legitimate client (Alice) script
├── server.py                # Original server (Bob) script
├── mitigate_client.py       # Secure client with identity verification
├── mitigate_server.py       # Secure server with mitigation logic
├── brute_force.py           # Brute-force login script (web login attacks)
```

## Requirements

* Python 3.x
* `pycryptodome` for AES encryption

Install dependencies:

```bash
pip install pycryptodome requests
```


## How to Run

### 1. Standard Protocol

Open two terminals:

**Terminal 1 (Bob - server):**

```bash
python server.py
```

**Terminal 2 (Alice - client):**

```bash
python client.py
```

---

### 2. Simulate Reflection Attack

**Terminal 1 (Bob - server):**

```bash
python server.py
```

**Terminal 2 (Trudy - attacker):**

```bash
python attacker.py
```

---

### 3. Run Mitigated Protocol

**Terminal 1 (Bob - secure server):**

```bash
python mitigate_server.py
```

**Terminal 2 (Alice - secure client):**

```bash
python mitigate_client.py
```

## Protocol Overview

### Challenge-Response Steps (Original)

1. Alice → Bob: `I am Alice | R_A`
2. Bob → Alice: `R_B | E(R_A, K_AB)`
3. Alice → Bob: `E(R_B, K_AB)`
4. Bob verifies R\_B

### Mitigated Steps

1. Alice → Bob: `I am Alice | R_A`
2. Bob → Alice: `R_B | E('Bob' + R_A, K_AB)`
3. Alice → Bob: `E('Alice' + R_B, K_AB)`
4. Bob verifies both identity and nonce


## Key Concepts

* **Reflection Attack**: An attacker reflects encrypted challenges to trick the server.
* **Nonce**: Random challenge to ensure freshness.
* **AES-128 Encryption (ECB Mode)**: Encrypts messages with a shared key.
* **Authentication**: Verifies identity by proving knowledge of shared secret.

# Code Demonstration

![Image](https://github.com/user-attachments/assets/2968ea81-b4e4-4eee-903c-b345ce47858b)
