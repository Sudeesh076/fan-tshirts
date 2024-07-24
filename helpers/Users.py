import uuid
from dataclasses import dataclass, asdict
from cryptography.fernet import Fernet

key = Fernet.generate_key()

@dataclass
class User:
    id: str
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str

    @classmethod
    def from_json(cls, data):
        required_fields = ['email', 'password', 'first_name', 'last_name', 'phone_number']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Missing required field: {field}')

        user_id = str(uuid.uuid4())
        encrypted_password = encrypt_password(data['password'])

        return cls(
            id=user_id,
            email=data['email'],
            password=encrypted_password,
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number']
        )

    def to_dict(self):
        return asdict(self)

@dataclass
class UserLogin:
    email: str
    password: str

    @classmethod
    def from_json(cls, data):
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Missing required field: {field}')
        encrypted_password = encrypt_password(data['password'])

        return cls(
            email=data['email'],
            password=encrypted_password,
        )

    def validatePassword(self,password):
        if decrypt_password(self.password)==decrypt_password(password):
            return True
        else:
            return False

@dataclass
class AdminLogin:
    email: str
    password: str

    @classmethod
    def from_json(cls, data):
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Missing required field: {field}')
        encrypted_password = encrypt_password(data['password'])

        return cls(
            email=data['email'],
            password=encrypted_password,
        )

    def validatePassword(self,password):
        if decrypt_password(self.password)==decrypt_password(password):
            return True
        else:
            return False


def encrypt_password(password):
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode('utf-8'))
    return encrypted_password.decode('utf-8')

def decrypt_password(encrypted_password):
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password.encode('utf-8'))
    return decrypted_password.decode('utf-8')
