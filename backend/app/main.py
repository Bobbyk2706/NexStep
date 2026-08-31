from fastapi import FastAPI

from app.routers.auth_router import router as auth_router

app = FastAPI(title="NexStep API")

app.include_router(auth_router)


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}