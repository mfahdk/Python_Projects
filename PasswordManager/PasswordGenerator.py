import string
import random
import secrets
from cryptography.fernet import Fernet

# Function to generate and save an encryption key to a file if it doesn't already exist
def writeKey():
    try:
        with open("key.key", "rb") as key_file:
            pass  # Check if the key file exists
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)  # Write the new key to a file

# Function to load the encryption key from the file
def loadKey():
    return open("key.key", "rb").read()

# Function to write encrypted password data to a file
def writeToFile(text, encMsg, path):
    with open(path, "a+") as file:
        i = 0
        for line in file:
            char = line.split(" - ")
            decrpyPass = key.decrypt(encMsg).decode('utf-8')  # Decrypt the password
            while decrpyPass[i] == char[1][i]:  # Ensure unique password
                i += 1
                password = passwordGenerator().encode('utf-8')
                encMsg = key.encrypt(password)
        
        # Write the encrypted website and password to the file
        write_line = f"{text.decode('utf-8')} - {encMsg.decode('utf-8')}\n"
        file.write(write_line)

# Function to generate a random secure password
def passwordGenerator():
    letters = string.ascii_uppercase + string.ascii_lowercase
    digits = string.digits
    specialChar = string.punctuation
    
    selection_list = letters + digits + specialChar
    passwordLength = 20  # Length of the generated password
    password = ''.join(secrets.choice(selection_list) for _ in range(passwordLength))
    return password

# Main function for the password manager
def main():
    writeKey()  # Ensure the encryption key is available
    f = loadKey()
    key = Fernet(f)
    
    # Path to the file storing encrypted passwords
    passwdPath = "PATH OF THE PASSWORD FILE"
    
    # User menu for password management options
    option = int(input("What do you want to do? \n1. Generate a password\n2. Read a generated password\nOption: "))
    if option == 1:  # Generate and save a new password
        with open(passwdPath, "a+") as file:
            text = input("What is the name of the website to add a password for = ")
            while text != "exit":
                password = passwordGenerator().encode('utf-8')
                encMsg = key.encrypt(password)
                text = text.encode('utf-8')
                websiteMsg = key.encrypt(text)

                writeToFile(websiteMsg, encMsg, passwdPath)
                text = input("What is the name of the website to add a password for = ")
    elif option == 2:  # Read stored passwords
        with open(passwdPath, "r") as file:
            for line in file:
                website, char = line.strip().split(" - ")
                text = website.encode('utf-8')
                encpassBytes = char.encode('utf-8')
                webpage = key.decrypt(website).decode('utf-8')  # Decrypt website name
                decrpyPass = key.decrypt(char).decode('utf-8')  # Decrypt password
                print("Website:", webpage, "\nPassword:", decrpyPass)
    print("Exiting Program")
    
if __name__ == "__main__":
    main()
