from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

engine = create_engine('mysql://root:ab?sad132FF..@localhost/mydb')
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column('id', Integer, primary_key=True)
    username = Column('username', String(45), unique=True)
    firstname = Column('firstname', String(45))
    lastname = Column('lastname', String(45))
    email = Column('email', String(45), unique=True)
    password = Column('password', String(200))
    phone = Column('phone', String(45), unique=True)
    role = Column('role', String(45))


class Event(Base):
    __tablename__ = "event"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(45), unique=True)
    address = Column('address', String(45))
    datatime = Column('datatime', DATETIME)
    tickets_count = Column('tickets_count', Integer)


class Ticket(Base):
    __tablename__ = "ticket"

    id = Column('id', Integer, primary_key=True)
    seat = Column('seat', Integer)
    type = Column('type', String(45))
    user_id = Column('user_id', ForeignKey(User.id))
    event_id = Column('event_id', ForeignKey(Event.id))
