from uvicorn import run
from fastapi import FastAPI
from app.api.routes import init_routes
from app.db.database_utils import initialize_database, seed_database

app = init_routes(FastAPI())

@app.get("/")
async def root():
    return {"message": "Welcome to the Stock Trading API 📈", "version": "1.0.0", "documentation_url": "/docs"}

@app.on_event("startup")
async def on_startup():
    await initialize_database()
    await seed_database()

if __name__ == "__main__":
    run("api.main:app")
