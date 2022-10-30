from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DATE
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

engine = create_engine('mysql://root:759486@localhost:3306/pp')
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()


class user(Base):
    __tablename__ = "user"

    iduser = Column('iduser', Integer, primary_key=True)
    username = Column('username', String(45))
    firstname = Column('firstname', String(45))
    lastname = Column('lastname', String(45))
    email = Column('email', String(45))
    password = Column('password', String(45))
    phone = Column('phone', String(45))
    role = Column('role', String(45))


class event(Base):
    __tablename__ = "event"

    idevent = Column('event', Integer, primary_key=True)
    adress = Column('adress', String(45))
    datatime = Column('datatime', String(45))
    tikets_count = Column('tikets_count', String(45))


class ticket(Base):
    __tablename__ = "ticket"

    idticket = Column('idticket', Integer, primary_key=True)
    seat = Column('seat', Integer)
    type = Column('type', String(45))
    user_id = Column('user_id', ForeignKey(user.iduser))
    event_id = Column('event_id', ForeignKey(event.idevent))
