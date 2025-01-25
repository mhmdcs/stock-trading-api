from uvicorn import run
from fastapi import FastAPI
from app.api.routes import init_routes
from app.db.database_utils import setup_db, seed_db

app = init_routes(FastAPI())

@app.get("/")
async def root():
    return {"message": "Welcome to the Stock Trading API 📈", "version": "1.0.0", "documentation_url": "/docs"}

@app.on_event("startup")
async def on_startup():
    await setup_db()
    await seed_db()

if __name__ == "__main__":
    run("app.api.main:app")
