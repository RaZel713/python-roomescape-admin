from typing import Dict, List, Optional
from models.time_model import Time
from models.reservation_model import Reservation, ReservationCreate

class Database:
    def __init__(self):
        self.times: Dict[int, Time] = {}
        self.reservations: Dict[int, Reservation] = {}
        self.time_counter = 1
        self.reservation_counter = 1

    def create_time(self, start_at: str) -> Time:
        time = Time(id=self.time_counter, startAt=start_at)
        self.times[self.time_counter] = time
        self.time_counter += 1
        return time

    def get_all_times(self) -> List[Time]:
        return list(self.times.values())

    def delete_time(self, time_id: int) -> bool:
        if time_id in self.times:
            del self.times[time_id]
            return True
        return False

    def get_time(self, time_id: int) -> Optional[Time]:
        return self.times.get(time_id)

    def create_reservation(self, reservation_data: ReservationCreate) -> Optional[Reservation]:
        time = self.get_time(reservation_data.timeId)
        if not time:
            return None
        
        reservation = Reservation(
            id=self.reservation_counter,
            date=reservation_data.date,
            name=reservation_data.name,
            timeId=reservation_data.timeId,
            time=time
        )
        self.reservations[self.reservation_counter] = reservation
        self.reservation_counter += 1
        return reservation

    def get_all_reservations(self) -> List[Reservation]:
        return list(self.reservations.values())

    def delete_reservation(self, reservation_id: int) -> bool:
        if reservation_id in self.reservations:
            del self.reservations[reservation_id]
            return True
        return False

# Create a single instance of the database
db = Database() 