from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers.auth_router import router as auth_router
from app.routers.eligibility_router import router as eligibility_router
from app.routers.profile_router import router as profile_router
from app.routers.eligibility_router import router as eligibility_router
from app.routers.profile_router import router as profile_router

app = FastAPI(title="NexStep API")

# Without this, the browser blocks every request from the Vite dev
# server (localhost:5173) to this API (localhost:8000) — different
# ports count as different origins. Add the deployed frontend's real
# URL here too once there is one.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend's default VITE_API_BASE_URL (see frontend/.env.example) is
# "http://localhost:8000/api" — mounting everything under /api here
# means the frontend works with zero config changes on their end.
app.include_router(auth_router, prefix="/api")
app.include_router(eligibility_router, prefix="/api")
app.include_router(profile_router, prefix="/api")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """FastAPI's default error body is {"detail": ...}. The frontend's
    fetch wrapper (src/api/client.js) reads data.message / data.error.
    Adding "message" alongside "detail" satisfies both without changing
    every route's error handling."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "message": exc.detail},
        headers=getattr(exc, "headers", None),
    )


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}