import os, sys
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from mysol.api import api_router
from mysol.database.middleware import DefaultSessionMiddleware

SECRET_KEY = os.urandom(32).hex()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://editorialhub.site", "https://www.editorialhub.site", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(DefaultSessionMiddleware)

@app.options("/{full_path:path}")
async def preflight_handler(request: Request, full_path: str):
    print(f"🔥 OPTIONS 요청 도착: {request.method} {request.url}")
    print(f"🔍 요청 헤더: {request.headers}")
    sys.stdout.flush()
    return Response(status_code=200)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}