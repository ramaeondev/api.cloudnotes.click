from fastapi import Depends, FastAPI
from app.routes import auth, note
from app.core.config import init_cors, init_db
from app.security import get_current_user
from mangum import Mangum
import json

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
        init_db()
    except Exception as e:
        print(f"Error during startup: {str(e)}")
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
_handler = Mangum(app)

# Wrapper function to handle both direct Lambda invocations and API Gateway events
def handler(event, context):
    try:
        # If this is a direct Lambda invocation (not through API Gateway)
        if 'httpMethod' not in event and 'path' not in event:
            # Return a simple response for health checks or direct invocations
            print("Direct Lambda invocation detected")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Lambda function is healthy'})
            }
        # Otherwise, pass to Mangum for API Gateway events
        return _handler(event, context)
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Internal Server Error: {str(e)}'})
        }