import hashlib
password = '123'
passhash = hashlib.sha256(password.encode()).hexdigest()
print(passhash)