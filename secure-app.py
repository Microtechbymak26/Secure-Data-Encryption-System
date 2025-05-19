
import streamlit as st
import hashlib
import json
import os
import time
from cryptography.fernet import Fernet

# --- Fixed Fernet Key (Paste your generated key here) ---
KEY = b'dtYuV5Fm88ivRqfrYNADd3z5MuPK3aK5_wZ9-gpi5Yo='# <-- Replace with your own key!
cipher = Fernet(KEY)
# --- Load/Save JSON Data (list structure) ---
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return []

def save_data():
    with open("data.json", "w") as f:
        json.dump(stored_data, f, indent=4)

# --- Hash Passkey ---
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# --- Initialize state ---
stored_data = load_data()  # Load existing data (list of dicts)
failed_attempts = 0
lockout_time = None

# --- Lockout check ---
def is_locked_out():
    global lockout_time
    if lockout_time and time.time() - lockout_time < 120:
        return True
    return False

# --- Encrypt data ---
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# --- Decrypt data ---
def decrypt_data(encrypted_text, passkey):
    global failed_attempts, lockout_time
    if is_locked_out():
        return "LOCKED"

    hashed_passkey = hash_passkey(passkey)

    for entry in stored_data:
        if entry["encrypted_text"] == encrypted_text and entry["passkey"] == hashed_passkey:
            failed_attempts = 0
            return cipher.decrypt(encrypted_text.encode()).decode()

    failed_attempts += 1
    if failed_attempts >= 3:
        lockout_time = time.time()
    return None

# --- Streamlit UI ---
st.title("🔒 Secure Data Encryption System")
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")

elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")
    user_data = st.text_area("Enter Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey:
            hashed_passkey = hash_passkey(passkey)
            encrypted_text = encrypt_data(user_data)
            # Append new record to list
            stored_data.append({"encrypted_text": encrypted_text, "passkey": hashed_passkey})
            save_data()
            st.success("✅ Data stored securely!")
            st.text_area("Encrypted Data (copy this to retrieve):", encrypted_text, height=100)
        else:
            st.error("⚠️ Both fields are required!")

elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    encrypted_text = st.text_area("Enter Encrypted Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_text and passkey:
            result = decrypt_data(encrypted_text, passkey)

            if result == "LOCKED":
                st.warning("⏳ Too many failed attempts. Please wait 2 minutes.")
            elif result:
                st.success(f"✅ Decrypted Data: {result}")
            else:
                st.error(f"❌ Incorrect passkey! Attempts remaining: {3 - failed_attempts}")
        else:
            st.error("⚠️ Both fields are required!")

elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    login_pass = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if login_pass == "admin123":  # Replace with secure auth in production
            failed_attempts = 0
            lockout_time = None
            st.success("✅ Reauthorized successfully! Redirecting to Retrieve Data...")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect password!")