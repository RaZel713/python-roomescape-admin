from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from models.time_model import TimeCreate, Time
from models.reservation_model import ReservationCreate, Reservation
from database.db import db


app = FastAPI()

# 정적 파일(Static files) 먼저 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

# 템플릿 경로 설정
templates = Jinja2Templates(directory="templates/admin")

@app.get("/", response_class=HTMLResponse)
async def admin_index(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/reservation", response_class=HTMLResponse)
async def admin_index(request: Request):
    return templates.TemplateResponse("reservation.html", {"request": request})

@app.get("/time", response_class=HTMLResponse)
async def admin_index(request: Request):
    return templates.TemplateResponse("time.html", {"request": request})

# Time API Endpoints
@app.post("/times", response_model=Time)
async def create_time(time: TimeCreate):
    return db.create_time(time.startAt)

@app.get("/times", response_model=list[Time])
async def get_times():
    return db.get_all_times()

@app.delete("/times/{time_id}")
async def delete_time(time_id: int):
    if db.delete_time(time_id):
        return JSONResponse(status_code=200, content={})
    raise HTTPException(status_code=404, detail="Time not found")

# Reservation API Endpoints
@app.post("/reservations", response_model=Reservation)
async def create_reservation(reservation: ReservationCreate):
    result = db.create_reservation(reservation)
    if not result:
        raise HTTPException(status_code=404, detail="Time slot not found")
    return result

@app.get("/reservations", response_model=list[Reservation])
async def get_reservations():
    return db.get_all_reservations()

@app.delete("/reservations/{reservation_id}")
async def delete_reservation(reservation_id: int):
    if db.delete_reservation(reservation_id):
        return JSONResponse(status_code=200, content={})
    raise HTTPException(status_code=404, detail="Reservation not found")
