from pydantic import BaseModel
from typing import Optional

class TimeBase(BaseModel):
    startAt: str

class TimeCreate(TimeBase):
    pass

class Time(TimeBase):
    id: int

    class Config:
        from_attributes = True 