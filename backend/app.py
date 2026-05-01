"""
FastAPI Application
===================
Main FastAPI application that:
- Initializes the healthcare simulation
- Mounts REST endpoints
- Configures CORS for the Next.js frontend

This is the main backend entry point started by Main.py.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.engine.simulation import HealthcareSimulation
from backend.api.routes import create_routes
from backend import config

# --- Global simulation ---
simulation = HealthcareSimulation(num_patients=config.DEFAULT_POPULATION)


# --- Create FastAPI app ---
app = FastAPI(
    title="Healthcare Simulation System",
    description="Healthcare network simulation with Normal and Pandemic modes (REST API)",
    version="2.0.0",
)

# --- CORS middleware for Next.js frontend ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Mount REST routes ---
router = create_routes(simulation)
app.include_router(router)


# --- Health check ---
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Healthcare Simulation System",
        "day": simulation.day,
        "mode": simulation.mode.mode,
    }
