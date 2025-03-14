from fastapi import Depends, FastAPI
from app.routes import auth, note
from app.core.config import init_cors, init_db
from app.security import get_current_user
from mangum import Mangum
import traceback
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create FastAPI instance
app = FastAPI(
    title="Cloudnotes api",
    version="1.0",
    description="API for work logging application",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Operations related to authentication",
        }
    ]
)
# Initialize CORS
init_cors(app)

# Initialize DB connection
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Starting DB initialization...")
        init_db()
        logger.info("DB initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")

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


# Create the Mangum handler
handler = Mangum(app)