from uvicorn import run
from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.routes import init_routes

app = init_routes(FastAPI())

@app.get("/")
async def root():
    return {"message": "Welcome to the Investor Bulletin API 📈", "version": "1.0.0", "documentation_url": "/docs"}

if __name__ == "__main__":
    run("api.main:app")
