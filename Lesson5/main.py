from fastapi import FastAPI
from db import Database
from router import user
from config import DB_URL

# Database obyektini yaratamiz
db = Database(DB_URL)

def create_app():
    app = FastAPI(
        title="User API",
        description="FastAPI CRUD with Asyncpg",
        version="1.0.0",
        openapi_url="/api/docs",
        redoc_url="/api/redoc",
        debug=True
    )

    # Routerni ulash
    app.include_router(user.router)

    # Start va shutdown hodisalarini qo‘shish
    @app.on_event("startup")
    async def startup():
        await db.connect()
        if db.pool is None:
            print("Database pool yaratilmadi! Ulanishni tekshiring.")
        else:
            print(f"Database pool: {db.pool}")  # Pool obyektining holatini tekshirish
        await db.create_table()


    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
