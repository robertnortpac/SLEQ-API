from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils.exceptions.base import (
    AppExceptionBase,
    http_exception_handler,
    request_validation_exception_handler,
    app_exception_handler,
)

from db.session import SessionLocal

app = FastAPI(
    title="SLEQ API",
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionBase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


# CORS and Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Routes
from api.routes import router as base_router

app.include_router(base_router)

from api.v1.routes import router as api_router

app.include_router(api_router, prefix="/api/v1")
