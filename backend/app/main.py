from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers.admin_review import router as admin_review_router
from app.routers.auth_router import router as auth_router
from app.routers.eligibility_router import router as eligibility_router
from app.routers.exam_router import router as exam_router
from app.routers.profile_router import router as profile_router
from app.routers.tracked_exam_router import router as tracked_exam_router


app = FastAPI(title="NexStep API")


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


app.include_router(
    auth_router,
    prefix="/api",
)

app.include_router(
    eligibility_router,
    prefix="/api",
)

app.include_router(
    profile_router,
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