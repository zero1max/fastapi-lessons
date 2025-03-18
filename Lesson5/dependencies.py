from fastapi import HTTPException
from db import Database
from config import DB_URL

# Create database instance
db = Database(DB_URL)

async def get_db() -> Database:
    """Dependency to get database instance"""
    if not db.pool:
        raise HTTPException(
            status_code=500,
            detail="Database connection not initialized"
        )
    return db 