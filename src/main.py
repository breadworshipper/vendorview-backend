from fastapi import FastAPI
from src.controllers.tracking import router as tracking_router
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.controllers.auth import auth_router
from src.controllers.item import items_router
from src.database import pool

app = FastAPI()
app.include_router(tracking_router)
app.include_router(auth_router)
app.include_router(items_router)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET")


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()


# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
