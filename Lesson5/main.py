from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from db import DatabaseError
from router import user
from config import DEBUG
from dependencies import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database connection pool
    try:
        await db.connect()
        await db.create_table()
        logger.info("Database initialized successfully")
        yield
    except DatabaseError as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    finally:
        # Shutdown: Close database connection
        await db.close()
        logger.info("Database connection closed")

app = FastAPI(
    title="User API",
    description="FastAPI CRUD with Asyncpg",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    debug=DEBUG,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)

@app.get("/")
async def root():
    """Root endpoint to check API status"""
    return {
        "status": "online",
        "message": "Welcome to User API",
        "docs_url": "/api/docs",
        "redoc_url": "/api/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
