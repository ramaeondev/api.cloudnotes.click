import os
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import ExpiredSignatureError, JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.db.models import User
from app.email_sender import send_email
from app.schemas import UserCreate
from app.schemas import StandardResponse
from app.db.database import get_db
import logging
import ulid


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
CONFIRMATION_TOKEN_EXPIRE_MINUTES = 60  # Token valid for 1 hour
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Refresh token valid for 7 days


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generates a JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_confirmation_token(email: str):
    """Generate an account confirmation token"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=CONFIRMATION_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def verify_confirmation_token(token: str):
    """Decode and validate the confirmation token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

@router.post("/register", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user and sends an email confirmation"""
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        id = ulid.new().str,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hashed_password,
        is_active=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate confirmation token
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    token = jwt.encode({"sub": new_user.email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

    # Dynamic confirmation URL
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    confirm_url = f"{BASE_URL}/v1/auth/confirm-email?token={token}"

    # Send confirmation email
    await send_email(
        to_email=new_user.email,
        subject="Confirm Your Email",
        body=f"Click the link to confirm your email: {confirm_url}"
    )
    return StandardResponse(
            isSuccess=True,
            messages=["User registered successfully"],
            errors=[],
            data={"user_id": new_user.id},
            status_code=status.HTTP_201_CREATED
        )

@router.post("/login", response_model=StandardResponse, status_code=status.HTTP_200_OK)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Handles user login and returns a JWT token"""
    logger.debug(f"Received login request for username: {form_data.username}")

    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        logger.warning(f"User not found: {form_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    logger.debug(f"Stored password hash: {user.password_hash}")
    is_password_correct = pwd_context.verify(form_data.password, user.password_hash)
    logger.debug(f"Password verification result: {is_password_correct}")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not confirmed. Please check your email.")

    if not is_password_correct:
        logger.warning(f"Invalid password for user: {user.email}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    logger.debug(f"Generated token: {access_token}")
    return StandardResponse(
        isSuccess=True, 
        message="Login successful", 
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "id": user.integer_id
            }
        }, 
        status_code=status.HTTP_200_OK
    )


@router.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    return {"message": "Database connection is working!"}

@router.get("/confirm-email")
def confirm_email(token: str, db: Session = Depends(get_db)):
    """Verifies email confirmation token and activates the user"""
    email = verify_confirmation_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_active:
        return StandardResponse(isSuccess=True,errors=[], messages=["Account already confirmed"],status_code=status.HTTP_200_OK)

    user.is_active = True  # Activate the user
    db.commit()

    return StandardResponse(isSuccess=True,errors=[], messages=["Email confirmed successfully! You can now log in."], status_code=status.HTTP_200_OK)

def create_refresh_token(data: dict):
    """Generates a refresh token with an extended expiration time"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)  + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_refresh_token