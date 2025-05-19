import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Example usage
hashed = hash_password("123456")
print(hashed)
