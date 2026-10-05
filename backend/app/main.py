import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers.admin_discovery import (
    router as admin_discovery_router,
)
from app.routers.admin_review import router as admin_review_router
from app.routers.auth_router import router as auth_router
from app.routers.chatbot_router import router as chatbot_router
from app.routers.eligibility_router import router as eligibility_router
from app.routers.exam_router import router as exam_router
from app.routers.profile_router import router as profile_router
from app.routers.notification_router import router as notification_router
from app.routers.tracked_exam_router import router as tracked_exam_router
from app.logging_config import setup_logging
from app.routers import admin_monitoring
from app.routers.admin_notifications import router as admin_notifications_router
from app.scheduler.notification_scheduler import (
    start_notification_scheduler,
    stop_notification_scheduler,
)
from contextlib import asynccontextmanager
from app.routers.signup_verification_router import router as signup_verification_router

setup_logging()




@asynccontextmanager
async def lifespan(app: FastAPI):
    start_notification_scheduler()
    try:
        yield
    finally:
        stop_notification_scheduler()


app = FastAPI(title="NexStep API", lifespan=lifespan)

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth_router,
    prefix="/api",
)

app.include_router(
    signup_verification_router,
    prefix="/api",
)

app.include_router(
    admin_monitoring.router,
    prefix="/api",
)

app.include_router(
    eligibility_router,
    prefix="/api",
)

app.include_router(
    chatbot_router,
    prefix="/api",
)

app.include_router(
    profile_router,
    prefix="/api",
)

app.include_router(
    notification_router,
    prefix="/api",
)

app.include_router(
    admin_review_router,
)

app.include_router(
    tracked_exam_router,
    prefix="/api",
)

app.include_router(
    exam_router,
    prefix="/api",
)
app.include_router(admin_discovery_router)

app.include_router(admin_notifications_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request,
    exc: HTTPException,
):
    """
    Return both FastAPI's standard `detail` field and
    a `message` field for frontend compatibility.
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "message": exc.detail,
        },
        headers=getattr(exc, "headers", None),
    )


@app.get("/")
def root():
    return {
        "status": "ok",
        "docs": "/docs",
    }