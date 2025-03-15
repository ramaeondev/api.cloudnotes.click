from fastapi import Depends, FastAPI, Response
from fastapi.responses import JSONResponse
from app.routes import auth, note
from app.core.config import get_config, init_cors, init_db
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
        },
        {
            "name": "Notes",
            "description": "Operations related to managing notes",
        }
    ]
)
# Initialize CORS
init_cors(app)
# ✅ Manually handle OPTIONS
from fastapi.responses import JSONResponse

@app.options("/{full_path:path}")
async def preflight_response():
    response = JSONResponse(content={"message": "CORS preflight successful"}, status_code=204)
    response.headers["Access-Control-Allow-Origin"] = "https://platform.cloudnotes.click"
    response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


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