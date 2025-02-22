from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine

def init_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update this in production!
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def init_db():
    Base.metadata.create_all(bind=engine)
