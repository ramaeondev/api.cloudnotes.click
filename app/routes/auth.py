from fastapi import APIRouter, HTTPException, Depends
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])  # Use the same tag name

@router.post("/signup")
def signup(username: str, password: str):
    hashed_password = hash_password(password)
    # Store `username` and `hashed_password` in the database
    return {"message": "User created successfully"}

@router.post("/login")
def login(username: str, password: str):
    # Fetch the hashed password from the database
    stored_hashed_password = "hashed-password-from-db"
    
    if not verify_password(password, stored_hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
