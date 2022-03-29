from condition_monitor import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBConnection(metaclass=Singleton):
    def __init__(self):
        self._engine = db
        Session = self._engine.session
        self.session = Session
    
    def flsuh(self):
        self.session.commit()

    def getRoom(self, name):
        return self.session.query(Room).filter(Room.name == name).first()

    def getRoomsForUser(self, id):
        access = self.session.query(Access).filter(Access.userid == id).all()
        ids = [acc.roomid for acc in access]
        return self.session.query(Room).filter(Room.id.in_(ids)).all()

    def getMeasurementsForRoom(self, id):
        return self.session.query(Measurement).filter(Measurement.roomid == id).all()
    
    def getLastMeasurementForRoom(self, id):
        return self.session.query(Measurement).filter(Measurement.roomid == id).order_by(Measurement.timestamp).first()
    
    def addUser(self, user):
        self._engine.session.add(user)
    
    def addRoom(self, room):
        self._engine.session.add(room)

class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(100))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False, unique = True)
    password_hash = db.Column(db.String(60), nullable = False)
    active = db.Column(db.Boolean(), nullable = False, default = True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Access(db.Model):
    __tablename__ = "accesses"
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable = False)
    user = db.relationship('User', backref=db.backref('accesses', cascade="all, delete"))
    roomid = db.Column(db.Integer, db.ForeignKey("rooms.id", ondelete='CASCADE'), nullable = False)
    room = db.relationship('Room', backref=db.backref('accesses', cascade="all, delete"))

class Measurement(db.Model):
    __tablename__ = "measurements"
    id = db.Column(db.Integer, primary_key = True)
    roomid = db.Column(db.Integer, db.ForeignKey("rooms.id", ondelete='CASCADE'))
    room = db.relationship('Room', backref=db.backref('measurements', cascade="all, delete"))
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)


