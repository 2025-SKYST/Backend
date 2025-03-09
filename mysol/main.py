import os
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from mysol.api import api_router
from mysol.database.middleware import DefaultSessionMiddleware

SECRET_KEY = os.urandom(32).hex()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://editorialhub.site", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"],
)


app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(DefaultSessionMiddleware)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.options("/{full_path:path}")
async def preflight_handler(full_path: str):
    return Response(status_code=200)