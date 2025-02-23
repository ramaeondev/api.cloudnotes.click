from datetime import datetime, timedelta, timezone
from jose import jwt
import os
import smtplib


SECRET_KEY = os.getenv("SECRET_KEY", "DonalTrumpIsTheBestPresident")

def create_reset_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(hours=1) 
    return jwt.encode({"sub": email, "exp": expire}, SECRET_KEY, algorithm="HS256")


def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
