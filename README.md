# Secure Data Encryption System

This project is a simple web application built with Streamlit that allows users to securely store and retrieve sensitive data using encryption and passkeys.

## Features

- Encrypt and store any text data securely.
- Retrieve and decrypt your data using your unique passkey.
- Data is protected with strong encryption (Fernet/AES).
- Lockout mechanism after 3 failed attempts (2-minute wait).
- Simple admin login to reset lockout.

## How It Works

1. **Store Data:**  
   - Enter your data and a passkey.
   - The data is encrypted and saved with a hash of your passkey.
   - You receive the encrypted text to use for retrieval.

2. **Retrieve Data:**  
   - Paste your encrypted text and enter your passkey.
   - If the passkey matches, your data is decrypted and shown.
   - After 3 wrong attempts, you must wait 2 minutes or login as admin to reset.

3. **Admin Login:**  
   - Use the "Login" menu to enter the master password (`admin123` by default) to reset failed attempts.

## How to Get Your Passkey and Encrypted Key

- **Passkey:**
  - When you store your data (in the "Store Data" section), you will be asked to enter a passkey of your choice. This passkey is used to encrypt and later decrypt your data. Remember this passkey, as you will need it to retrieve your data.

- **Encrypted Key (Encrypted Data):**
  - After you store your data, the app will display an "Encrypted Data" field. This is your encrypted key (actually, the encrypted version of your data). Copy and save this encrypted text somewhere safe.

- **Retrieving Data:**
  - To get your original data back, go to the "Retrieve Data" section, paste your saved encrypted key into the "Enter Encrypted Data" box, and enter your passkey. If both are correct, your data will be decrypted and shown.

## How to Run

1. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the App:**
   ```bash
   streamlit run secure-app.py
   ```

3. **Open in Browser:**  
   The app will open in your default browser. Use the sidebar to navigate.

## Files

- `secure-app.py` : Main Streamlit application.
- `data.json` : Stores encrypted data and hashed passkeys.
- `requirements.txt` : Python dependencies.

## Security Note

- The encryption key and admin password are hardcoded for demo purposes.  
  For real use, store secrets securely and use proper authentication.

## Imported Modules Explanation

The following Python modules are imported in this project:

- `streamlit`: For building the web app interface.
- `hashlib`: For hashing the passkey securely.
- `json`: For reading and writing data to the JSON file.
- `os`: For checking file existence and handling file operations.
- `time`: For managing lockout timing after failed attempts.
- `cryptography.fernet` (Fernet): For encrypting and decrypting the data securely.

These modules together help in creating a secure, interactive, and user-friendly data encryption system. 