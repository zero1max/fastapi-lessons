import asyncpg

class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.db_url)
        print("Database connection pool created!")

    async def create_table(self):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    full_name text NOT NULL,
                    username varchar(225) UNIQUE NOT NULL,
                    email varchar(100) UNIQUE NOT NULL,
                    password varchar(255) NOT NULL
                )
            ''')
            print("Table 'users' created successfully!")

    async def add(self, full_name: str,username: str, email:str, password:str)->list[dict]:
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO users (full_name,username,email,password) VALUES ($1, $2, $3, $4)",
                full_name,
                username,
                email,
                password
            )
            return [{
                "fullname": full_name,
                "username": username,
                "email" : email,
                "password" : password
            }]


    async def all(self) -> list[dict]:
        async with self.pool.acquire() as conn:
            users = await conn.fetch("SELECT * FROM users")
            return [dict(user) for user in users]

    async def is_exists(self, user_id: int) -> bool:
        async with self.pool.acquire() as conn:
            user = await conn.fetchval("SELECT EXISTS(SELECT 1 FROM users WHERE user_id = $1)", user_id)
            return user

    async def update(self, user_id: int, new_name: str) -> int:
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "UPDATE users SET full_name = $1 WHERE user_id = $2", new_name, user_id
            )
            return result

    async def delete(self, user_id: int) -> int:
        async with self.pool.acquire() as conn:
            result = await conn.execute("DELETE FROM users WHERE user_id = $1", user_id)
            return result

    async def close(self):
        if self.pool:
            await self.pool.close()
            print("Database connection pool closed!")
