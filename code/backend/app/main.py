from fastapi.responses import HTMLResponse, FileResponse
import os

@app.get("/", response_class=HTMLResponse)
def serve_ui_direct():
    target = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(target):
        return open(target, encoding="utf-8").read()
    return "<h2>DocShield Bharat AI Engine Online</h2>"
from fastapi.responses import FileResponse, HTMLResponse
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router

app = FastAPI(title="DocShield AI Omega API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    index_p = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_p):
        return HTMLResponse(content=open(index_p, encoding="utf-8").read())
    return HTMLResponse("<h1>DocShield Bharat AI Console</h1>")

@app.get("/health")
def health():
    return {"status": "healthy"}

app.include_router(api_router, prefix="/api/v1")



