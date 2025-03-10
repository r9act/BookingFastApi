import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRegister(BaseModel):
    name: str
    surname: str


class UserGet(BaseModel):
    first_name: str = ""
    surname: str = ""
    recommended_by: Optional["UserGet"] = None

    # Pydantic 1.x: Использует классический способ настройки через class Config.
    # Pydantic 2.x: Вводит новый способ с помощью ConfigDict для более структурированного подхода к настройке моделей.
    class Config:
        orm_mode = True


class BookingGet(BaseModel):
    member_id: int
    member: UserGet
    facility_id: int
    start_time: datetime.datetime
    slots: int

    model_config = ConfigDict(from_attributes=True)


class BookingCreate(BaseModel):
    facility_id: int
    member_id: int
    start_time: datetime.datetime
    slots: int

    class Config:
        from_attributes = True


class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    surname: Optional[str] = None
    address: Optional[str] = None
    zipcode: Optional[str] = None
    telephone: Optional[str] = None
    recommended_by_id: Optional[int] = None

    class Config:
        from_attributes = True
