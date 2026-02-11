"""Utility script to generate hashed password for streamlit-authenticator"""
import bcrypt

print("Generate hashed password for streamlit-authenticator")
print("=" * 50)

password = input("Enter password to hash: ")
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

print(f"\nHashed password:\n{hashed}")
print("\nAdd this to your Railway environment variables as AUTH_PASSWORD_HASH")
print("Or update run_local.sh.production with this hash for local use")
