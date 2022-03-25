from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from condition_monitor import app

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBConnection(metaclass=Singleton):
    def __init__(self):
        self._engine = SQLAlchemy(app)
        self._session = self._engine.session
    
    def flsuh(self):
        self._session.commit()

    def getRoom(self, name):
        return self._session.query(Room).filter(Room.name == name).first()

    def getRoomsForUser(self, id):
        access = self._session.query(Access).filter(Access.user == id).all()
        ids = [acc.room for acc in access]
        return self._session.query(Room).filter(Room.id.in_(ids)).all()

    def getMeasurementsForRoom(self, id):
        return self._session.query(Measurement).filter(Measurement.room == id).all()
    
    def getLastMeasurementForRoom(self, id):
        return self._session.query(Measurement).filter(Measurement.room == id).order_by(Measurement.timestamp).first()

model = DBConnection()._engine.Model

class Room(model):
    __tablename__ = "rooms"
    id = Column(Integer(), primary_key = True)
    name = Column(String(10), unique=True, nullable=False)
    description = Column(String(100))

class User(model):
    __tablename__ = "users"
    id = Column(Integer(), primary_key = True)
    username = Column(String(30), nullable = False, unique = True)
    email = Column(String(50), nullable = False, unique = True)
    password_hash = Column(String(60), nullable = False)

class Access(model):
    __tablename__ = "accesses"
    id = Column(Integer(), primary_key = True)
    user = Column(Integer(), ForeignKey("users.id", ondelete='SET NULL'))
    room = Column(Integer(), ForeignKey("rooms.id", ondelete='SET NULL'))

class Measurement(model):
    __tablename__ = "measurements"
    id = Column(Integer(), primary_key = True)
    room = Column(Integer(), ForeignKey("rooms.id", ondelete='SET NULL'))
    temperature = Column(Integer())
    humidity = Column(Float())
    timestamp = Column(DateTime())