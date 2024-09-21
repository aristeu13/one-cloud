from fastapi import FastAPI, Depends
from app.application.api.api import api_router
from app.core.middleware.db import get_db

app =  FastAPI(title="one-cloud")

app.include_router(api_router)


@app.get("/health")
def check_health():
    return {"status": True}
