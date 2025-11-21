import hashlib
import secrets
import base64
import os

class User:
    def __init__(self, name, password=None):
        self.name = name
        self.salt = None
        self.hashed_password = None
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.salt = secrets.token_bytes(16)  # 16-byte salt
        self.hashed_password = hashlib.scrypt(
            password.encode('utf-8'),
            salt=self.salt,
            n=16384,  # CPU/memory cost (2**14)
            r=8,      # Block size
            p=1,      # Parallelism
            dklen=64  # Output length
        )

    def check_password(self, password):
        if not self.hashed_password:
            return False
        test_hash = hashlib.scrypt(
            password.encode('utf-8'),
            salt=self.salt,
            n=16384,
            r=8,
            p=1,
            dklen=64
        )
        return test_hash == self.hashed_password

    def get_name(self):
        return self.name

    def save(self):
        if not self.hashed_password:
            raise ValueError("No password set to save.")
        file_path = f'userdata/{self.name}.txt'
        os.makedirs('userdata', exist_ok=True)  # Ensure directory exists
        with open(file_path, 'w') as f:
            f.write(f'Name: {self.name}\n')
            f.write(f'Salt: {base64.b64encode(self.salt).decode("utf-8")}\n')
            f.write(f'Hashed_Password: {base64.b64encode(self.hashed_password).decode("utf-8")}\n')
        os.chmod(file_path, 0o600)  # Restrict to owner read/write

    @staticmethod
    def load(file_path):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                name = lines[0].split(': ')[1].strip()
                salt_b64 = lines[1].split(': ')[1].strip()
                hashed_b64 = lines[2].split(': ')[1].strip()
                user = User(name)
                user.salt = base64.b64decode(salt_b64)
                user.hashed_password = base64.b64decode(hashed_b64)
                return user
        except FileNotFoundError:
            print(f"User file '{file_path}' not found.")
            return None
        except (IndexError, ValueError):
            print(f"Invalid file format in '{file_path}'.")
            return None

    def __str__(self):
        return f"User(name={self.name}, password_hash={'*' * 8 if self.hashed_password else None})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, User):
            return (self.name == other.name and
                    self.salt == other.salt and
                    self.hashed_password == other.hashed_password)
        return False