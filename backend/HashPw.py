import bcrypt

# Password to hash
password = "1234".encode('utf-8')

# Generate the hashed password
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# Print the hashed password
print(hashed.decode('utf-8'))