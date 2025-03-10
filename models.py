from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import SessionLocal

Baza = declarative_base()


# наследуемся от базового класса Baza - это и есть ORM - мэпим класс (object) с релиционной таблицой (relation)
# O-R mapping

class Member(Baza):
    # начинается с двойного подчеркивания (__) не потому, что это магическое имя или специальный синтаксис SQLAlchemy,
    # а потому, что это соглашение об именовании, которое указывает, что это атрибут, специфичный для ORM.
    __tablename__ = "members"
    __table_args__ = {"schema": "cd"}

    id = Column(Integer, primary_key=True, name="memid")
    surname = Column(String)
    first_name = Column(String, name="firstname")
    address = Column(String)
    zipcode = Column(String)
    telephone = Column(String)
    recommended_by_id = Column(
        Integer, ForeignKey("cd.members.memid"), name="recommendedby"
    )
    # recommended_by используется в schemas
    recommended_by = relationship("Member", remote_side=[id])
    join_date = Column(TIMESTAMP, name="joindate")


class Facility(Baza):
    __tablename__ = "facilities"
    __table_args__ = {"schema": "cd"}
    id = Column(Integer, primary_key=True, name="facid")
    name = Column(String)
    member_cost = Column(Float, name="membercost")
    guest_cost = Column(Float, name="guestcost")
    initial_outlay = Column(Float, name="initialoutlay")
    monthly_maintenance = Column(Float, name="monthlymaintenance")


class Booking(Baza):
    __tablename__ = "bookings"
    __table_args__ = {"schema": "cd"}
    id = Column(Integer, primary_key=True, name="bookid", autoincrement=True)
    facility_id = Column(
        Integer, ForeignKey("cd.facilities.facid"), primary_key=True, name="facid"
    )
    facility = relationship("Facility")
    member_id = Column(
        Integer, ForeignKey("cd.members.memid"), primary_key=True, name="memid"
    )
    member = relationship("Member")
    start_time = Column(TIMESTAMP, name="starttime")
    slots = Column(Integer)


# Использование конструкции if __name__ == "__main__": в Python нужно для того, чтобы указать, какие части кода
# должны выполняться, только если данный файл запускается непосредственно, а не импортируется как модуль в другой файл.

# Когда файл запускается напрямую, переменная __name__ автоматически получает значение "__main__", и код внутри блока
# выполняется. Когда файл импортируется в другом файле, переменная __name__ будет иметь значение, соответствующее
# имени этого модуля, и код внутри блока не будет выполнен.
if __name__ == "__main__":
    session = SessionLocal()
    results = (
        session.query(Booking)
        .join(Member)
        .filter(Member.first_name == "Tim")
        .limit(5)
        .all()
    )
    for x in results:
        print(f"name = {x.member.zipcode}, start_time = {x.start_time}")
