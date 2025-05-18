# Brute Force Login Script

This Python script performs a **brute-force login attack** on a web application's login form by attempting multiple passwords from a given wordlist. It's built using the `requests` module and is designed for **educational and ethical penetration testing purposes only**.

> **DISCLAIMER**:
> This tool is intended for **authorized testing only**. Do not use it against systems you do not own or have explicit permission to test. Unauthorized use is illegal and unethical.

## 🚀 Features

* Automates login attempts using a username and a password list.
* Detects rate-limiting based on response content.
* Handles network exceptions gracefully.
* Uses a persistent session for efficiency.

## Requirements

* Python 3.x
* `requests` library

Install the required dependency with:

```bash
pip install requests
```

## Usage

```bash
python brute_force.py <url> <username> <password_file>
```

### Example

```bash
python brute_force.py http://localhost/process_login.php admin passwords.txt
```


## How It Works

1. Reads passwords from a file.
2. Sends HTTP POST requests to the login URL with each password.
3. Looks for success or failure responses.
4. Stops if a successful login is detected or if rate-limiting is encountered

# Code Demonstration

![Image](https://github.com/user-attachments/assets/e0e3f4d2-f8bb-4fe9-815d-b577182a2a44)
