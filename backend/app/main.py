"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router

app = FastAPI(
    title="Quantum Intelligence Learning Lab",
    description="SIH26140 — AI-Based Interactive Quantum Algorithm Learning Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "service": "Quantum Intelligence Learning Lab API (Eureka Forge)",
        "status": "online",
        "version": "0.1.0",
        "docs_url": "/docs",
        "health_url": "/api/v1/health",
        "frontend_url": "http://localhost:3000",
        "message": "Backend API is active. Visit http://localhost:3000 to view the interactive web platform, or /docs for API documentation."
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "quantum-intelligence-lab", "simulator_ready": True}
