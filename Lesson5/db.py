import asyncpg
from typing import Optional, List, Dict, Any
from passlib.context import CryptContext
import logging
from datetime import datetime
from asyncpg.pool import Pool
import asyncio

# Configure logging
logger = logging.getLogger(__name__)

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DatabaseError(Exception):
    """Base exception for database errors"""
    pass

class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool: Optional[Pool] = None
        self._init_retries = 3
        self._init_retry_interval = 5  # seconds

    async def connect(self) -> None:
        """Create database connection pool with retry logic"""
        retry_count = 0
        while retry_count < self._init_retries:
            try:
                self.pool = await asyncpg.create_pool(
                    self.db_url,
                    min_size=5,
                    max_size=20,
                    command_timeout=60,
                    timeout=30
                )
                logger.info("Database connection pool created successfully!")
                break
            except Exception as e:
                retry_count += 1
                if retry_count == self._init_retries:
                    logger.error(f"Failed to create database pool after {self._init_retries} attempts: {str(e)}")
                    raise DatabaseError(f"Database connection failed: {str(e)}")
                logger.warning(f"Failed to create pool, attempt {retry_count} of {self._init_retries}")
                await asyncio.sleep(self._init_retry_interval)

    async def create_table(self) -> None:
        """Create necessary database tables"""
        if not self.pool:
            raise DatabaseError("Database connection not initialized")
            
        try:
            async with self.pool.acquire() as conn:
                # Create users table
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        full_name TEXT NOT NULL,
                        username VARCHAR(20) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP WITH TIME ZONE,
                        is_active BOOLEAN DEFAULT TRUE,
                        CONSTRAINT username_check CHECK (username ~ '^[a-zA-Z0-9_-]+$'),
                        CONSTRAINT email_check CHECK (email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
                    )
                ''')

                # Create updated_at trigger
                await conn.execute('''
                    CREATE OR REPLACE FUNCTION update_updated_at_column()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        NEW.updated_at = CURRENT_TIMESTAMP;
                        RETURN NEW;
                    END;
                    $$ language 'plpgsql';
                ''')

                await conn.execute('''
                    DROP TRIGGER IF EXISTS update_users_updated_at ON users;
                    CREATE TRIGGER update_users_updated_at
                        BEFORE UPDATE ON users
                        FOR EACH ROW
                        EXECUTE FUNCTION update_updated_at_column();
                ''')

                logger.info("Database tables and triggers created successfully!")
        except Exception as e:
            logger.error(f"Failed to create database tables: {str(e)}")
            raise DatabaseError(f"Table creation failed: {str(e)}")

    async def add(self, full_name: str, username: str, email: str, password: str) -> Dict[str, Any]:
        """Add a new user to the database"""
        if not self.pool:
            raise DatabaseError("Database connection not initialized")

        try:
            hashed_password = pwd_context.hash(password)
            
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    user = await conn.fetchrow(
                        """
                        INSERT INTO users (full_name, username, email, password) 
                        VALUES ($1, $2, $3, $4)
                        RETURNING id, full_name, username, email, created_at, updated_at, is_active
                        """,
                        full_name, username.lower(), email.lower(), hashed_password
                    )
                    return dict(user)
        except asyncpg.UniqueViolationError as e:
            logger.error(f"Unique constraint violation: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to add user: {str(e)}")
            raise DatabaseError(f"Failed to create user: {str(e)}")

    async def all(self) -> List[Dict[str, Any]]:
        """Retrieve all active users"""
        if not self.pool:
            raise DatabaseError("Database connection not initialized")

        try:
            async with self.pool.acquire() as conn:
                users = await conn.fetch(
                    """
                    SELECT id, full_name, username, email, created_at, updated_at, is_active
                    FROM users 
                    WHERE is_active = TRUE
                    ORDER BY created_at DESC
                    """
                )
                return [dict(user) for user in users]
        except Exception as e:
            logger.error(f"Failed to fetch users: {str(e)}")
            raise DatabaseError(f"Failed to fetch users: {str(e)}")

    async def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve user by ID"""
        if not self.pool:
            raise DatabaseError("Database connection not initialized")

        try:
            async with self.pool.acquire() as conn:
                user = await conn.fetchrow(
                    """
                    SELECT id, full_name, username, email, created_at, updated_at, is_active
                    FROM users 
                    WHERE id = $1 AND is_active = TRUE
                    """,
                    user_id
                )
                return dict(user) if user else None
        except Exception as e:
            logger.error(f"Failed to fetch user: {str(e)}")
            raise DatabaseError(f"Failed to fetch user: {str(e)}")

    async def update(self, user_id: int, full_name: str = None, email: str = None, password: str = None) -> Optional[Dict[str, Any]]:
        """Update user information by ID"""
        if not self.pool:
            raise DatabaseError("Database connection not initialized")

        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    updates = []
                    values = []
                    if full_name:
                        updates.append(f"full_name = ${len(values) + 1}")
                        values.append(full_name)
                    if email:
                        updates.append(f"email = ${len(values) + 1}")
                        values.append(email.lower())
                    if password:
                        updates.append(f"password = ${len(values) + 1}")
                        values.append(pwd_context.hash(password))
                    
                    if not updates:
                        return None

                    values.append(user_id)
                    query = f"""
                        UPDATE users 
                        SET {', '.join(updates)}
                        WHERE id = ${len(values)} AND is_active = TRUE
                        RETURNING id, full_name, username, email, created_at, updated_at, is_active
                    """
                    user = await conn.fetchrow(query, *values)
                    return dict(user) if user else None
        except asyncpg.UniqueViolationError:
            logger.error("Email already exists")
            raise
        except Exception as e:
            logger.error(f"Failed to update user: {str(e)}")
            raise DatabaseError(f"Failed to update user: {str(e)}")

    async def delete(self, user_id: int) -> bool:
        """Soft delete a user by ID"""
        if not self.pool:
            raise DatabaseError("Database connection not initialized")

        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    result = await conn.execute(
                        """
                        UPDATE users 
                        SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
                        WHERE id = $1 AND is_active = TRUE
                        """,
                        user_id
                    )
                    return 'UPDATE 1' in result
        except Exception as e:
            logger.error(f"Failed to delete user: {str(e)}")
            raise DatabaseError(f"Failed to delete user: {str(e)}")

    async def verify_password(self, username: str, password: str) -> bool:
        """Verify user password"""
        if not self.pool:
            raise DatabaseError("Database connection not initialized")

        try:
            async with self.pool.acquire() as conn:
                stored_password = await conn.fetchval(
                    """
                    SELECT password 
                    FROM users 
                    WHERE username = $1 AND is_active = TRUE
                    """,
                    username.lower()
                )
                if stored_password is None:
                    return False
                return pwd_context.verify(password, stored_password)
        except Exception as e:
            logger.error(f"Failed to verify password: {str(e)}")
            raise DatabaseError(f"Failed to verify password: {str(e)}")

    async def update_last_login(self, username: str) -> None:
        """Update user's last login timestamp"""
        if not self.pool:
            raise DatabaseError("Database connection not initialized")

        try:
            async with self.pool.acquire() as conn:
                await conn.execute(
                    """
                    UPDATE users 
                    SET last_login = CURRENT_TIMESTAMP 
                    WHERE username = $1 AND is_active = TRUE
                    """,
                    username.lower()
                )
        except Exception as e:
            logger.error(f"Failed to update last login: {str(e)}")
            raise DatabaseError(f"Failed to update last login: {str(e)}")

    async def close(self) -> None:
        """Close database connection pool"""
        if self.pool:
            try:
                await self.pool.close()
                logger.info("Database connection pool closed successfully!")
            except Exception as e:
                logger.error(f"Error closing database pool: {str(e)}")
                raise DatabaseError(f"Failed to close database connection: {str(e)}")
