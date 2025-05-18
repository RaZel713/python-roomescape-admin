# main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.views import admin
from app.api import reservation, time

app = FastAPI(debug=True)

# Static files configuration
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates configuration
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(reservation.router, prefix="/reservations", tags=["reservations"])
app.include_router(time.router, prefix="/times", tags=["times"])

# Root redirect
@app.get("/")
async def root():
    return RedirectResponse(url="/admin/")

# Debug endpoint
@app.get("/debug")
async def debug():
    return {
        "routes": [
            {"path": route.path, "name": route.name} 
            for route in app.routes
        ]
    }