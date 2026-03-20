"""Generate a password hash for testing"""
import bcrypt

# Generate hash for password 'testpass123'
password = 'testpass123'
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
print(f"Password: {password}")
print(f"Hash: {hashed}")
print("\nSet this as AUTH_PASSWORD_HASH environment variable")
