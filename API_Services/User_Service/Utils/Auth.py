from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from config import (
    JWT_SECRET,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)

# -------------------------------------
# PASSWORD HASHING (bcrypt)
# -------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------------------
# TOKEN GENERATION HELPERS
# -------------------------------------
def _create_token(data: Dict[str, Any], expires_delta: timedelta, token_type: str) -> str:
    """
    Internal helper to create JWT tokens with expiry and type.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Create a short-lived access token (used for authentication).
    """
    return _create_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), "access")


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a long-lived refresh token (used to generate new access tokens).
    """
    return _create_token(data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), "refresh")


# -------------------------------------
# TOKEN DECODING & VALIDATION
# -------------------------------------
def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode token and return payload, or None if invalid.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Validate if token is a valid access token.
    """
    payload = decode_token(token)
    if payload and payload.get("type") == "access":
        return payload
    return None


def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Validate if token is a valid refresh token.
    """
    payload = decode_token(token)
    if payload and payload.get("type") == "refresh":
        return payload
    return None


# -------------------------------------
# OTP VALIDATION (Email / Phone)
# -------------------------------------
def verify_otp(provided_otp: str, stored_otp: str) -> bool:
    """
    Verify if provided OTP matches stored OTP.
    """
    return provided_otp == stored_otp


# -------------------------------------
# CAPTCHA VALIDATION (Server-side)
# -------------------------------------
def verify_captcha(captcha_token: str) -> bool:
    """
    Placeholder for captcha verification.
    In production, call Google reCAPTCHA or hCaptcha API here.
    """
    # Example: send captcha_token to provider API and check response
    # For now, return True if token exists
    return bool(captcha_token)
