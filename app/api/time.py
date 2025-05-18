from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from typing import List
import datetime

router = APIRouter()

class TimeCreate(BaseModel):
    startAt: str

    @validator('startAt')
    def validate_time_format(cls, v):
        try:
            datetime.datetime.strptime(v, "%H:%M")
            return v
        except ValueError:
            raise ValueError("시간은 HH:MM 형식이어야 합니다 (예: 14:30)")

class Time(TimeCreate):
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "startAt": "14:30"
            }
        }

# 인메모리 데이터베이스
class InMemoryDB:
    def __init__(self):
        self.current_id = 0
        self.times = {}
    
    def get_next_id(self):
        self.current_id += 1
        return self.current_id
    
    def create(self, time_data: TimeCreate) -> Time:
        time_id = self.get_next_id()
        new_time = Time(id=time_id, startAt=time_data.startAt)
        self.times[time_id] = new_time
        return new_time
    
    def get_all(self) -> List[Time]:
        return list(self.times.values())
    
    def get_by_id(self, time_id: int) -> Time:
        if time_id not in self.times:
            raise HTTPException(status_code=404, detail="예약 시간을 찾을 수 없습니다")
        return self.times[time_id]
    
    def delete(self, time_id: int):
        if time_id not in self.times:
            raise HTTPException(status_code=404, detail="예약 시간을 찾을 수 없습니다")
        del self.times[time_id]

# 인메모리 데이터베이스 인스턴스 생성
db = InMemoryDB()

# 전역 변수로 times 노출 (reservation.py에서 사용)
times = db.times

@router.post("/", response_model=Time)
async def create_time(time: TimeCreate):
    """새로운 예약 시간을 생성합니다."""
    return db.create(time)

@router.get("/", response_model=List[Time])
async def get_times():
    """모든 예약 시간을 조회합니다."""
    return db.get_all()

@router.delete("/{time_id}")
async def delete_time(time_id: int):
    """특정 예약 시간을 삭제합니다."""
    db.delete(time_id)
    return {"message": "예약 시간이 성공적으로 삭제되었습니다"}