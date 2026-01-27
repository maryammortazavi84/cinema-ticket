import hashlib
import os

password = "mypassword"
salt = os.urandom(16)  # 16 بایت رشته تصادفی

password_bytes = password.encode("utf-8") + salt
hash_object = hashlib.sha256(password_bytes)
hash_hex = hash_object.hexdigest()

print(hash_hex)
print(salt.hex())  # برای ذخیره کردن کنار هش

