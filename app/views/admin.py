from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def admin_home(request: Request):
    return templates.TemplateResponse("admin/index.html", {"request": request})

@router.get("/reservation", response_class=HTMLResponse)
async def admin_reservation(request: Request):
    return templates.TemplateResponse("admin/reservation.html", {"request": request})

@router.get("/time", response_class=HTMLResponse)
async def admin_time(request: Request):
    return templates.TemplateResponse("admin/time.html", {"request": request})