from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date
from .time import Time, times

router = APIRouter()

class ReservationBase(BaseModel):
    name: str
    date: date
    time_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "홍길동",
                "date": "2024-03-18",
                "time_id": 1
            }
        }

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    time: Time

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "홍길동",
                "date": "2024-03-18",
                "time_id": 1,
                "time": {
                    "id": 1,
                    "startAt": "14:30"
                }
            }
        }

# 인메모리 데이터베이스
class InMemoryDB:
    def __init__(self):
        self.current_id = 0
        self.reservations = {}
    
    def get_next_id(self):
        self.current_id += 1
        return self.current_id
    
    def create(self, reservation_data: ReservationCreate) -> Reservation:
        if reservation_data.time_id not in times:
            raise HTTPException(status_code=404, detail="존재하지 않는 예약 시간입니다")
            
        reservation_id = self.get_next_id()
        new_reservation = Reservation(
            id=reservation_id,
            name=reservation_data.name,
            date=reservation_data.date,
            time_id=reservation_data.time_id,
            time=times[reservation_data.time_id]
        )
        self.reservations[reservation_id] = new_reservation
        return new_reservation
    
    def get_all(self) -> List[Reservation]:
        return list(self.reservations.values())
    
    def get_by_id(self, reservation_id: int) -> Reservation:
        if reservation_id not in self.reservations:
            raise HTTPException(status_code=404, detail="예약을 찾을 수 없습니다")
        return self.reservations[reservation_id]
    
    def delete(self, reservation_id: int):
        if reservation_id not in self.reservations:
            raise HTTPException(status_code=404, detail="예약을 찾을 수 없습니다")
        del self.reservations[reservation_id]

# 인메모리 데이터베이스 인스턴스 생성
db = InMemoryDB()

@router.post("/", response_model=Reservation)
async def create_reservation(reservation: ReservationCreate):
    """새로운 예약을 생성합니다."""
    return db.create(reservation)

@router.get("/", response_model=List[Reservation])
async def get_reservations():
    """모든 예약 목록을 조회합니다."""
    return db.get_all()

@router.get("/{reservation_id}", response_model=Reservation)
async def get_reservation(reservation_id: int):
    """특정 예약을 조회합니다."""
    return db.get_by_id(reservation_id)

@router.delete("/{reservation_id}")
async def delete_reservation(reservation_id: int):
    """특정 예약을 삭제합니다."""
    db.delete(reservation_id)
    return {"message": "예약이 성공적으로 삭제되었습니다"}