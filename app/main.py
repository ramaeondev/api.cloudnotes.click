from fastapi import FastAPI
from app.routes import auth
from app.core.config import init_cors, init_db

# Create FastAPI instance
app = FastAPI(title="Logit API", version="1.0")

# Initialize DB and CORS
init_db()
init_cors(app)

# Include Routes
app.include_router(auth.router, prefix="/auth")

@app.get("/")
def read_root():
    return {"message": "Welcome to Logit API!"}