# Description
### **Secure Encrypted Password Manager**
  
This Python-based password management application is designed to securely generate, store, and retrieve passwords. It leverages the `cryptography` library's `Fernet` encryption to protect sensitive data from unauthorized access. With features for generating strong passwords and securely storing them, this program provides a user-friendly way to manage credentials while prioritizing security.

**Key Features:**  
1. **Password Generation**: Creates strong, 20-character-long passwords with a mix of uppercase, lowercase, digits, and special characters.  
2. **Encryption**: Protects passwords and website names using symmetric encryption.  
3. **Data Storage**: Stores encrypted passwords in a specified file (`passwords.txt`).  
4. **User-Friendly Menu**: Provides an intuitive interface for adding new passwords and retrieving stored ones.  

**Enhancements for Improved Security:**  
1. **Hidden Storage Folder**: Enhance security by storing the `passwords.txt` file in a hidden folder to prevent accidental discovery:  
   - On Windows: Use the command `attrib +h folder_name` to make the folder hidden.  
   - On Linux/macOS: Prefix the folder name with a dot (e.g., `.secure_folder`).  
   Store both `passwords.txt` and `key.key` in this hidden folder for an additional layer of security.  

2. **Environment-Specific Key Storage**: Avoid storing the encryption key in a file by leveraging environment variables or secure storage methods:  
   - Set the key as an environment variable and retrieve it during runtime. For example, on Linux/macOS, use `export KEY=your_key` in your terminal.  
   - Use secure vaults like AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault for professional-grade key management.  

By incorporating these enhancements, users can significantly improve the safety and reliability of their password management system, creating a secure and scalable solution for safeguarding credentials.

# Code Demonstration

![passwordMangaer](https://github.com/user-attachments/assets/1edd1047-f46e-440e-8e9b-e85e0002caa1)
