from fastapi import Depends, FastAPI
from app.routes import auth, note
from app.core.config import init_cors, init_db
from app.security import get_current_user
from mangum import Mangum
import json
import traceback
import sys

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
async def startup_event():
    try:
        print("Starting DB initialization...")
        init_db()
        print("DB initialization completed successfully")
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        # Log the error but don't fail startup completely

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
_handler = Mangum(app, lifespan="off")

# Wrapper function to handle both direct Lambda invocations and API Gateway events
def handler(event, context):
    try:
        print(f"Event received: {json.dumps(event)}")
        
        # If this is a direct Lambda invocation (not through API Gateway)
        if 'httpMethod' not in event and 'path' not in event:
            # Return a simple response for health checks or direct invocations
            print("Direct Lambda invocation detected")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Lambda function is healthy'})
            }
        
        # For API Gateway request
        print(f"Processing API Gateway request for path: {event.get('path', 'unknown')}")
        return _handler(event, context)
    except Exception as e:
        error_detail = traceback.format_exc()
        print(f"Error in handler: {str(e)}")
        print(f"Traceback: {error_detail}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Internal Server Error',
                'error': str(e),
                'traceback': error_detail
            })
        }