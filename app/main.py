from fastapi import Depends, FastAPI
from app.routes import auth, note
from app.core.config import init_cors, init_db
from app.security import get_current_user
from mangum import Mangum

# Create FastAPI instance
app = FastAPI(
    title="Logit API",
    version="1.0",
    description="API for work logging application",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Operations related to authentication",
        }
    ]
)
init_cors(app) 
# Initialize DB and CORS during startup
@app.on_event("startup")
def startup_event():
    init_db()
    
@app.get("/")
def read_root():
    return {"message": "Welcome to Logit API!"}

# Secure endpoint
@app.get("/secure-endpoint", tags=["Authentication"])
def secure_endpoint(user=Depends(get_current_user)):
    return {"message": "You are authenticated!", "user": user.dict()}

# Include Routes
app.include_router(auth.router)
app.include_router(note.router)
handler = Mangum(app)
