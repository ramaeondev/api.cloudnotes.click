from fastapi import FastAPI
from app.routes import auth, users  # Import your routes
from .db import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Initialize the database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI instance
app = FastAPI(title="Logit API", version="1.0")

# Enable CORS (for frontend to communicate)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")

@app.get("/")
def read_root():
    return {"message": "Welcome to Logit API!"}