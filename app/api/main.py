from uvicorn import run
from fastapi import FastAPI
from api.routes import init_routes

app = init_routes(FastAPI())

@app.get("/")
async def root():
    return {"message": "Welcome to the Investor Bulletin API 📈", "version": "1.0.0", "documentation_url": "/docs"}

if __name__ == "__main__":
    run("api.main:app")
