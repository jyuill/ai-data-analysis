"""Utility script to generate hashed password for streamlit-authenticator"""
import streamlit_authenticator as stauth

print("Generate hashed password for streamlit-authenticator")
print("=" * 50)

password = input("Enter password to hash: ")
hashed = stauth.Hasher([password]).generate()[0]

print(f"\nHashed password:\n{hashed}")
print("\nAdd this to your Railway environment variables as AUTH_PASSWORD_HASH")
