import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from app.api.v1.router import api_router

app = FastAPI(
    title="DocShield AI API",
    description="Zero-Trust Identity Screening Infrastructure",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    candidates = [
        os.path.join(os.path.dirname(__file__), "index.html"),
        os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "index.html"),
        "code/backend/app/index.html",
        "code/frontend/index.html",
        "frontend/index.html",
        "index.html"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    return HTMLResponse(content=f.read())
            except Exception:
                pass
    return HTMLResponse("<h2>DocShield Bharat AI Engine Online</h2>")

app.include_router(api_router, prefix="/api")
