from pydantic import BaseModel
from time_model import Time

class ReservationBase(BaseModel):
    date: str
    name: str
    timeId: int

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    time: Time

    class Config:
        from_attributes = True