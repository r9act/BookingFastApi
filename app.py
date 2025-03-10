from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Booking, Facility, Member
from schemas import BookingGet, UserGet, BookingCreate, MemberUpdate
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "First FastAPI app"}


def get_db():
    with SessionLocal() as db:
        return db


@app.get("/user/all", response_model=List[UserGet])
def get_all_users(limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Member).limit(limit).all()


@app.get("/facility/all")
def get_all_facilities(limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Facility).limit(limit).all()


@app.get("/booking/all", response_model=List[BookingGet])
def get_all_bookings(limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Booking).limit(limit).all()


@app.post("/booking/", response_model=BookingGet)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    # Проверяем, существуют ли Facility и Member для нового бронирования
    facility = db.query(Facility).filter(Facility.id == booking.facility_id).first()
    member = db.query(Member).filter(Member.id == booking.member_id).first()

    if not facility:
        logging.debug("Facility not found, raising 404")
        raise HTTPException(status_code=404, detail="Facility not found")
    if not member:
        logging.debug("Member not found, raising 404")
        raise HTTPException(status_code=404, detail="Member not found")

    # Создаем новую запись о бронировании
    new_booking = Booking(
        facility_id=booking.facility_id,
        member_id=booking.member_id,
        start_time=booking.start_time,
        slots=booking.slots
    )

    # Добавляем запись в базу данных и сохраняем изменения
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)  # Обновляем объект для получения данных после commit

    return new_booking


@app.put("/user/{member_id}", response_model=UserGet)
def update_member(member_id: int, member_update: MemberUpdate, db: Session = Depends(get_db)):
    # Fetch the member from the database
    member = db.query(Member).filter(Member.id == member_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Update fields if they are provided
    if member_update.first_name is not None:
        member.first_name = member_update.first_name
    if member_update.surname is not None:
        member.surname = member_update.surname
    if member_update.address is not None:
        member.address = member_update.address
    if member_update.zipcode is not None:
        member.zipcode = member_update.zipcode
    if member_update.telephone is not None:
        member.telephone = member_update.telephone
    if member_update.recommended_by_id is not None:
        member.recommended_by_id = member_update.recommended_by_id

    # Commit the changes
    db.commit()
    db.refresh(member)  # Refresh to get the updated instance

    return member


@app.delete("/user/{member_id}", status_code=204)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    # Fetch the member from the database
    member = db.query(Member).filter(Member.id == member_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Delete the member
    db.delete(member)
    db.commit()

    # No content to return
    return None


uvicorn.run(app, host="127.0.0.1", port=8899)
