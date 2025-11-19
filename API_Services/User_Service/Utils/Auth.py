# Utils/Auth.py
from jose import JWTError
import jwt
from datetime import datetime, timedelta
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

# No hashing, no verification
def hash_password(password: str) -> str:
    return password  # store raw password

def verify_password(plain_password: str, stored_password: str) -> bool:
    return plain_password == stored_password  # simple compare

# JWT token creation
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
